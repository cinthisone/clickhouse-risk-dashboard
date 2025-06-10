# Installing ClickHouse on WSL (Windows Subsystem for Linux)

This guide documents how ClickHouse was installed on WSL (Ubuntu), including troubleshooting steps and solutions for common issues.

---

## 1. Update System Packages
```bash
sudo apt-get update
sudo apt-get upgrade
```

## 2. Install Required Dependencies
```bash
sudo apt-get install apt-transport-https ca-certificates dirmngr
```

## 3. Add ClickHouse Repository Key
```bash
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 8919F6BD2B48D754
```
> **Note:** You may see a warning that `apt-key` is deprecated. This is safe to ignore for now, but future versions of Ubuntu may require a different approach.

## 4. Add ClickHouse Repository
```bash
echo "deb https://packages.clickhouse.com/deb stable main" | sudo tee /etc/apt/sources.list.d/clickhouse.list
```

## 5. Install ClickHouse Server and Client
```bash
sudo apt-get update
sudo apt-get install clickhouse-server clickhouse-client
```

## 6. Start ClickHouse Server
```bash
sudo service clickhouse-server start
```

## 7. Set/Reset Default User Password (if needed)
If you see authentication errors (e.g., `Authentication failed: password is incorrect, or there is no user with such name`), reset the default password:
```bash
sudo rm /etc/clickhouse-server/users.d/default-password.xml
sudo service clickhouse-server restart
```
This will reset the password for the `default` user to empty (no password).

## 8. Test the Installation
```bash
clickhouse-client --query "SELECT 1"
```
You should see:
```
1
```

## 9. Enable HTTP Interface (for Python clients)
By default, ClickHouse listens on port 8123 for HTTP. Confirm with:
```bash
sudo netstat -tulnp | grep 8123
```
You should see something like:
```
tcp        0      0 127.0.0.1:8123          0.0.0.0:*               LISTEN      <pid>/clickhouse-s
```

## 10. Troubleshooting

### Problem: Authentication Failed
- **Symptom:** `Authentication failed: password is incorrect, or there is no user with such name.`
- **Fix:** Remove the password file and restart the server (see step 7).

### Problem: HTTPDriver returned response code 400
- **Symptom:** Python client errors like `DatabaseError: HTTPDriver for http://localhost:9000 returned response code 400`.
- **Fix:**
  - Use port `8123` (HTTP) in your Python scripts, not `9000` (native protocol).
  - Example:
    ```python
    clickhouse_connect.get_client(host='localhost', port=8123, username='default', password='', database='your_db')
    ```

### Problem: Download Button Locked on Yahoo Finance
- **Symptom:** Can't download CSVs directly from Yahoo Finance due to a lock icon/paywall.
- **Fix:** Use the `yfinance` Python package to download data programmatically.

### Problem: Data Ingestion Errors (KeyError, ValueError)
- **Symptom:** Errors when ingesting CSVs, e.g., `KeyError: 1` or `ValueError: could not convert string to float`.
- **Fix:**
  - Ensure your CSVs are clean (no extra header rows, correct columns).
  - Update ingestion scripts to skip problematic rows and convert data types as needed.

---

## References
- [ClickHouse Official Installation Guide](https://clickhouse.com/docs/en/getting-started/install/)
- [ClickHouse Troubleshooting](https://clickhouse.com/docs/en/operations/troubleshooting/)

---

Feel free to add your own notes and issues as you learn more! 