import streamlit as st
import polars as pl  # type: ignore 
import matplotlib.pyplot as plt
import requests
import pandas as pd
import io


# ------------------------------------------------------------ Function to read CSV or Excel ---------------------------------------------------------------------------
# Baca fail menggunakan Polars kerana Polars tidak menggunakan memori yang tinggi
def process_file(uploaded_file):
    """Reading CSV or Excel files with Polars."""
    if uploaded_file.name.endswith('.csv'):
        df = pl.read_csv(uploaded_file)  
    else:
        df = pl.read_excel(uploaded_file)  
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


    # -------------------------------------- Checking that 'Source IP' and 'Destination IP' exist before classification ------------------------------------------------
    # Untuk baca colum Source and Destination
    # Verify Traffic either Internal or External
    if "Source IP" in df.columns and "Destination IP" in df.columns:
        df = df.with_columns([
            pl.struct(["Source IP", "Destination IP"]).map_elements(
                lambda row: classify_traffic(row["Source IP"], row["Destination IP"])
            ).alias("Traffic Type"),
            pl.col("Source IP").map_elements(mark_private_ip).alias("Source IP"),
            pl.col("Destination IP").map_elements(mark_private_ip).alias("Destination IP")
        ])
    else:
        st.error("Error: 'Source IP' or 'Destination IP' column not found.")

    return df
    # ------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------ Inbound or Outbound -------------------------------------------------------------------------
# Function to determine Inbound or Outbound based on Source IP and Destination IP
def classify_traffic(source_ip, dest_ip):
    """determine Inbound or Outbound based on Source IP and Destination IP."""
    private_ip_ranges = ["10.", "172.16.", "192.168."]
    
    source_is_private = any(str(source_ip).startswith(p) for p in private_ip_ranges)
    dest_is_private = any(str(dest_ip).startswith(p) for p in private_ip_ranges)

    if not source_is_private and dest_is_private:
        return "Inbound"
    elif source_is_private and not dest_is_private:
        return "Outbound"
    else:
        return "Internal"
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ---------------------------------------------------------------------------- Private IP ------------------------------------------------------------------------------
# Mark Private IP as (Private IP)
# Example: 10.1.1.10 (Private IP)
def mark_private_ip(ip):
    """Marking the IP as a Private IP if necessary."""
    private_ip_ranges = ["10.", "172.16.", "192.168."]
    ip = str(ip)
    return f"{ip} (Private IP)" if any(ip.startswith(p) for p in private_ip_ranges) else ip
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------

# --------------------------------------------------------------------------- API Key VirusTotal -----------------------------------------------------------------------
# Virustotal akan baca semua IP yang ada dalam Log
# Kalau ada 50 IP, VT akan baca 50 IP walaupun ianya IP repeated
def check_virustotal(ip):
    """Checking IP with VirusTotal + ASN + Network Provider."""
    API_KEY = "3f6ea52674a36e14dd9e8498f602d9e399f6a0d799bcdc29956aa0fd0ef33ce9"
    url = f"https://www.virustotal.com/api/v3/ip_addresses/{ip}"
    headers = {"x-apikey": API_KEY}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        attributes = data.get("data", {}).get("attributes", {})
        
        # Dapatkan status Malicious
        malicious = "Malicious" if attributes.get("last_analysis_stats", {}).get("malicious", 0) > 0 else "Clean"
        
        # Dapatkan ASN dan Network Provider
        asn = attributes.get("asn", "Unknown ASN")
        network_provider = attributes.get("as_owner", "Unknown Provider")
        
        return f"{malicious} [{asn} - {network_provider}]"
    
    return "Unknown"
# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------ API Key AbuseIPDB ---------------------------------------------------------------------
# AbuseIPDB akan baca semua IP 
# Kalau ada 50 IP, Abuse akan baca 50 IP walaupun ianya IP repeated
def check_abuseip(ip):
    """Check IP reputation from AbuseIPDB."""
    API_KEY = "875a62f5eb57f49bf35394537ff3aa28f18635cc199d53bc43ca95af742c152ece27f7c4ce1ecc26"
    #875a62f5eb57f49bf35394537ff3aa28f18635cc199d53bc43ca95af742c152ece27f7c4ce1ecc26
    url = f"https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&maxAgeInDays=90"
    headers = {"Key": API_KEY, "Accept": "application/json"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "status": "Malicious" if data["data"]["abuseConfidenceScore"] > 50 else "Clean",
            "confidence": data["data"]["abuseConfidenceScore"]
        }
    
    return {"status": "Unknown", "confidence": 0}

# Format Output 
def format_abuseip_result(result):
    """Format output AbuseIPDB  'Malicious - 85%' or 'Clean - 0%'."""
    return f"{result['status']} - {result['confidence']}%"
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------ Highlight ----------------------------------------------------------------------------
# Highlight warna merah kalau IP Itu Malicious
# Example: VT - Malicious & Abuse - Clean = Highlight Red
def highlight_row(row):
    virus_total = str(row["VirusTotal"]).strip() if pd.notna(row["VirusTotal"]) else ""
    abuse_ip = str(row["AbuseIP"]).strip() if pd.notna(row["AbuseIP"]) else ""

    if "Malicious" in virus_total or "Malicious" in abuse_ip:
        return ['background-color: #b60808; color: white;'] * len(row)
    return [''] * len(row)
# ---------------------------------------------------------------------------------------------------------------------------------------------------------------------


# ------------------------------------------------------------------------------ Dashboard ----------------------------------------------------------------------------
def generate_dashboard(df):
    """Display Dashboard"""
    st.markdown(
        "<h1 style='text-align: center; color: #b60808; font-size: 40px;'>📊 Log Analyzer Dashboard</h1><hr style='border:2px solid #b60808'>", 
        unsafe_allow_html=True
    )
    
    # ===================================================================== Detect time column ========================================================================
    time_col = None
    for col in df.columns:
        if 'time' in col.lower().replace(" ", ""):  # remove space & check lowercase
            time_col = col
            break

    if time_col is None:
        st.warning("⚠️ Time column not found.")
    else:
        try:
            # Cleaning Spcae
            df = df.with_columns([
                pl.col(time_col).str.strip_chars().alias(time_col)
            ])

            # Format 24-Hours
            df = df.with_columns([
                pl.col(time_col).str.strptime(pl.Datetime, format="%d/%m/%Y %H:%M", strict=False).alias("Parsed_Time")
            ])

            # Display Time Range
            start_time = df["Parsed_Time"].min()
            end_time = df["Parsed_Time"].max()

            if start_time is not None and end_time is not None:
                st.info(f"🕒 Time Range: {start_time.strftime('%d %b %Y [%I:%M %p]')} - {end_time.strftime('%d %b %Y [%I:%M %p]')}")
            else:
                st.warning("No valid time data found in the time column.")
        except Exception as e:
            st.error(f"Failed to parse time column: {e}")
    # =================================================================================================================================================================

    # ========================================================================= Layout Grid ===========================================================================
    # Layout guna columns sebab nak ada banyak benda dalam satu baris

    # Col1 & Col2 untuk Pie Cart Inbound Outbound and Source IP & Destination IP 
    col1, col2 = st.columns([1, 3])  
    
    with col1:
        # Pie Chart for Inbound vs Outbound Traffic
        if 'Traffic Type' in df.columns:
            traffic_counts = df["Traffic Type"].value_counts()
            fig, ax = plt.subplots(figsize=(3, 3))  
            ax.pie(traffic_counts["count"].to_list(), labels=traffic_counts["Traffic Type"].to_list(), autopct='%1.1f%%', colors=['#8B0000', '#00008B'])  
            st.pyplot(fig)
        else:
            st.error("Error: 'Traffic Type' column not found.")

    # ======================================================================== Top 5 Source IP ======================================================================
    with col2:
    # Top 5 Source IP
        st.subheader("Top 5 Source IP")
        source_ip_counts = df.group_by(["Source IP", "Traffic Type", "Action"]).agg(pl.len().alias("count")).sort("count", descending=True).head(5)

        # Check VirusTotal dan AbuseIP
        source_ip_counts = source_ip_counts.with_columns([
            pl.col("Source IP").map_elements(check_virustotal).alias("VirusTotal"),
            pl.col("Source IP").map_elements(lambda ip: format_abuseip_result(check_abuseip(ip))).alias("AbuseIP"),
        ])

        st.dataframe(source_ip_counts)  

        # Button for full view
        with st.expander("🔍 View All Source IP (15 Row Only)"):
            all_source_ip = (
                df.group_by(["Source IP", "Traffic Type", "Action"])
                .agg(pl.len().alias("count"))  # Kira bilangan setiap Source IP
                .sort("count", descending=True)  # Susun ikut bilangan tertinggi
                .head(15)
            )
            all_source_ip = all_source_ip.with_columns([
                pl.col("Source IP").map_elements(check_virustotal).alias("VirusTotal"),
                pl.col("Source IP").map_elements(lambda ip: format_abuseip_result(check_abuseip(ip))).alias("AbuseIP"),
            ])

            # Pastikan count dimasukkan ke dalam DataFrame
            all_source_ip = all_source_ip.select(["Source IP", "Traffic Type", "Action", "count", "VirusTotal", "AbuseIP"])

            all_source_ip_pd = all_source_ip.to_pandas()

            # Highlight Malicious / Blacklisted
            st.dataframe(all_source_ip_pd.style.apply(highlight_row, axis=1), use_container_width=True)

        # ===============================================================================================================================================================

        # ======================================================= Top 5 Destination IP ============================================================================
        st.subheader("Top 5 Destination IP")

        # Pastikan "Destination IP" ada dalam DataFrame sebelum digunakan
        if "Destination IP" in df.columns:
            dest_ip_counts = df.group_by(["Destination IP", "Traffic Type", "Action"]).agg(pl.len().alias("count")).sort("count", descending=True).head(5)

            # Semakan VirusTotal dan AbuseIP untuk Destination IP
            dest_ip_counts = dest_ip_counts.with_columns([
                pl.col("Destination IP").map_elements(check_virustotal).alias("VirusTotal"),
                pl.col("Destination IP").map_elements(lambda ip: format_abuseip_result(check_abuseip(ip))).alias("AbuseIP"),
            ])

            st.dataframe(dest_ip_counts)
            with st.expander("🔍 View All Destination IP (15 Row Only)"):
                all_dest_ip = (
                    df.group_by(["Destination IP", "Traffic Type", "Action"])
                    .agg(pl.len().alias("count"))  # Kira bilangan setiap Destination IP
                    .sort("count", descending=True)  # Susun ikut bilangan tertinggi
                    .head(15)
                )
                all_dest_ip = all_dest_ip.with_columns([
                    pl.col("Destination IP").map_elements(check_virustotal).alias("VirusTotal"),
                    pl.col("Destination IP").map_elements(lambda ip: format_abuseip_result(check_abuseip(ip))).alias("AbuseIP"),
                ])
                # Pastikan count dimasukkan ke dalam DataFrame
                all_dest_ip = all_dest_ip.select(["Destination IP", "Traffic Type", "Action", "count", "VirusTotal", "AbuseIP"])

                all_dest_ip_pd = all_dest_ip.to_pandas()
                # Highlight Malicious / Blacklisted
                st.dataframe(all_dest_ip_pd.style.apply(highlight_row, axis=1), use_container_width=True)

        else:
            st.error("Error: 'Destination IP' column not found.")
    # ===============================================================================================================================================================

    # ========================================================== Action Block or Allowed ============================================================================
    st.subheader("Action 'Block or Allowed'")
    col3, col4 = st.columns([1, 3])
    
    with col3:
        if 'Action' in df.columns:
            # Value Counts
            action_counts = df["Action"].value_counts()

            # Convert ke Dictionary
            action_dict = dict(zip(action_counts["Action"].to_list(), action_counts["count"].to_list()))

            # Kira total dengan .get() supaya selamat
            allowed_count = action_dict.get("allowed", 0)
            block_count = action_dict.get("blocked", 0)

            # Pie Chart
            fig, ax = plt.subplots(figsize=(2, 2))  
            ax.pie(
                action_counts["count"].to_list(), 
                labels=action_counts["Action"].to_list(), 
                autopct='%1.1f%%', 
                colors=['#FF0000', '#008000'],
                textprops={'fontsize': 6}
            )  
            st.pyplot(fig)

            # Display Metric
            colA, colB = st.columns(2)
            colA.metric("Total Allowed", allowed_count)
            colB.metric("Total Block", block_count)
        else:
            st.error("Error: 'Action' column not found.")

    # ===============================================================================================================================================================

    # ===================================================================== Signature Section =======================================================================
    with col4:
        st.subheader("List of Signature")

        # Top 5 Signature
        signature_counts = (
            df.group_by("Signature")
            .agg([
                pl.col("Action").first().alias("Action"),
                pl.col("Category").first().alias("Category"),   # <-- Tambah Category
                pl.len().alias("Count")
            ])
            .sort("Count", descending=True)
            .head(5)
        )

        signature_counts_pd = signature_counts.to_pandas()

        st.dataframe(signature_counts_pd, use_container_width=True)

        # View All Signature (Expander)
        with st.expander("🔍 View All Signature"):
            signature_all = (
                df.group_by("Signature")
                .agg([
                    pl.col("Action").first().alias("Action"),
                    pl.col("Category").first().alias("Category"),  # <-- Tambah Category
                    pl.len().alias("Count")
                ])
                .sort("Count", descending=True)
            )

            signature_all_pd = signature_all.to_pandas()

            # FUNCTION untuk highlight row block sahaja
            def highlight_block(row):
                if row["Action"].lower() == "block" or row["Action"].lower() == "blocked":
                    return ['background-color: #b60808'] * len(row)   # warna light red
                else:
                    return [''] * len(row)

            st.dataframe(
                signature_all_pd.style.apply(highlight_block, axis=1),
                use_container_width=True
            )

    # ===============================================================================================================================================================
    st.markdown("""
    <hr style="border:1px solid #b60808; margin-top:15px; margin-bottom:15px;">
    """, unsafe_allow_html=True)

    # Full Data Table (Keluar dari col4 untuk jadikan full-width)
    st.subheader("Full Log Details")
    
    total_logs = df.shape[0]
    st.write(f"Total Log Entries: **{total_logs}**")

    default_columns = ["Time", "Traffic Type", "Source IP", "Source Country", "Destination IP", "Destination Country", "Destination Port", "Signature", "Category", "Action",]
    existing_columns = df.columns
    missing_columns = [col for col in default_columns if col not in existing_columns]

    for col in missing_columns:
        df = df.with_columns(pl.lit("Unknown").alias(col))

    df_full = df.select(default_columns)
        
    st.dataframe(df_full.to_pandas(), use_container_width=True)
    
    # ===============================================================================================================================================================

st.set_page_config(layout="wide")  
st.title("Upload Log File")

# ================== COMPILER ===================
st.subheader("🛠️ Excel Compiler Section")

# ===================== GARISAN CUSTOM =====================
st.markdown("""
<style>
.line-custom {
    width: 100%;
    height: 2px;
    background: #45a29e;
    box-shadow: 0 0 16px #45a29e;
    border: none;
    margin-top: 15px;
    margin-bottom: 15px;
    border-radius: 2px;
}
</style>

<div class="line-custom"></div>
""", unsafe_allow_html=True)


with st.container():
    st.markdown('<div class="compilebox">', unsafe_allow_html=True)

    compiler_files = st.file_uploader("📂 Upload files for compilation (Min 2 files)", type=["xlsx", "csv"], accept_multiple_files=True, key="compiler")

    if compiler_files:
        if len(compiler_files) > 1:
            if st.button("⚙️ Compile and Download"):
                dfs = []
                for file in compiler_files:
                    if file.name.endswith(".xlsx"):
                        df_part = pd.read_excel(file)
                    elif file.name.endswith(".csv"):
                        df_part = pd.read_csv(file)
                    else:
                        continue
                    dfs.append(df_part)

                compiled_df = pd.concat(dfs, ignore_index=True)
                compiled_excel = io.BytesIO()
                compiled_df.to_excel(compiled_excel, index=False)
                compiled_excel.seek(0)

                st.success("✅ Compilation successful! Click below to download.")

                st.download_button("📥 Download Compiled Excel", data=compiled_excel, file_name="compiled_logs.xlsx")

                st.info("⚠️ Please upload the compiled file below (Upload Log File) for analysis.")
        else:
            st.warning("⚠️ Please upload at least 2 files to compile.")

    # ===================== GARISAN =====================
    st.markdown("""
    <hr style="border:1px solid #45a29e; margin-top:15px; margin-bottom:15px;">
    """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)


# ================== ORIGINAL ===================
uploaded_file = st.file_uploader("Upload your file for Analyst", type=["xlsx", "csv"])  

if uploaded_file:
    df = process_file(uploaded_file)  
    generate_dashboard(df)

#"c:/Users/anonymous/Desktop/Testing/Version 2/System.py"