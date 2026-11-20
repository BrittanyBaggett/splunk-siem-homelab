# Splunk SIEM Homelab

## Overview

This project documents my hands-on experience building and configuring a Splunk SIEM homelab on Windows 11.

The purpose of this lab is to develop practical skills in security log collection, SPL querying, detection engineering, and security monitoring. The lab includes Windows Event Log analysis, a custom authentication detection rule, and integration with a Python-based file modification monitor.

## Lab Environment

**Operating System**: Windows 11

**Tools and Technologies:**
- Splunk Enterprise
- Splunk Universal Forwarder
- Windows Event Logs
- Splunk Search Processing Language (SPL)
- Python

## 1. Splunk Installation and Configuration

Installed Splunk Enterprise and the Splunk Universal Forwarder on a Windows 11 machine.

Configured the Universal Forwarder to send logs to Splunk Enterprise and verified successful ingestion of:

- Windows Security Event Logs
- Windows System Event Logs
- Windows Application Event Logs
- System performance metrics, including CPU, memory, disk, and network activity
- Used Splunk's Search & Reporting application to explore the collected events.


## 2. Windows Security Log Analysis

Practiced writing SPL queries to search, filter, and analyze Windows Security events.

## Security Events Investigated

|Event ID|Description|
|---|---|
|4624|Successful logon|
|4625|Failed logon|
|4648|Logon attempted using explicit credentials|
|4672|Special privileges assigned to a new logon|

## Example SPL Queries

**Identify the most common Windows Security events:**

index=main sourcetype="WinEventLog:Security"<br>
| stats count by EventCode<br>
| sort -count<br>

**Investigate successful logons:**

index=main sourcetype="WinEventLog:Security" EventCode=4624<br>
| table _time EventCode LogName ComputerName Account_Name Logon_Process<br>

**Investigate failed logons:**

index=main sourcetype="WinEventLog:Security" EventCode=4625<br>
| table _time ComputerName EventCode Account_Name<br>
| sort -_time<br>

## 3. Detection Engineering

## Failed Authentication Detection

Created a scheduled Splunk alert to identify accounts with five or more failed authentication attempts within one hour.

**Detection logic:**

index=main sourcetype="WinEventLog:Security" EventCode=4625 <br>
| stats count as FailedAttempts by Account_Name<br>
| where FailedAttempts >= 5<br>

**Alert configuration:**
- Alert type: Scheduled
- Schedule: Every hour
- Search window: Last 1 hour
- Trigger condition: Number of results greater than 0
- Trigger frequency: Once
- Action: Add to Triggered Alerts

**Detection Testing**
- Generated five failed authentication attempts on the Windows 11 machine.
- Verified that Windows recorded failed authentication events using Event ID 4625.
- Confirmed that the events appeared in Splunk Enterprise.
- Reviewed the SPL detection logic and alert threshold.
- Validation status: Event generation and ingestion confirmed. Scheduled alert triggering remains to be confirmed and documented.

**4. Python File Modification Monitoring** 

Developed a Python script using the Watchdog library to monitor filesystem modifications.

The script uses a custom event handler that inherits from FileSystemEventHandler and overrides the on_modified() method.

**Features**
- Monitors a specified Windows directory.
- Detects file modification events.
- Filters out directory modification events.
- Records modified file paths.
- Uses Python's logging module to write events to file_monitor.log.
- Includes timestamps and logging severity levels.

**Example Log Output**

2026-11-18 15:39:26,466 INFO: C:\Lab\Text1.txt | File Modified

**Splunk Integration**

Configured the Splunk Universal Forwarder to monitor the Python-generated log file.

Example inputs.conf configuration:

[monitor://C:\Lab\file_monitor.log]<br>
disabled = 0<br>
index = main<br>
sourcetype = file_monitor<br>

Restarted the Universal Forwarder to apply the configuration and verified that file modification events appeared in Splunk Enterprise.

**Verification search:**

index=main sourcetype="file_monitor"

This integration demonstrates the collection of custom application logs in addition to native Windows Event Logs.

## 5. Skills Developed

**Splunk and SIEM**
- Splunk Enterprise configuration
- Universal Forwarder configuration
- Windows Event Log ingestion
- Custom log source integration
- SPL searching and aggregation
- Scheduled detection rule creation

**Python and Security Monitoring**
- Python classes and inheritance
- Event-driven programming
- Watchdog observers and event handlers
- Filesystem modification monitoring
- Python logging
- Integration of custom logs with a SIEM

## 6. Future Improvements
- Complete scheduled alert validation
- Extract structured fields from Python-generated file modification logs
- Create file modification detection rules
- Install Sysmon for additional endpoint visibility
- Investigate process creation and network connection events
- Develop Splunk security monitoring dashboards
- Document security investigations and detection results
