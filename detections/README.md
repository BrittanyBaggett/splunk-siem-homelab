# Detection Rules

This folder contains SPL detection rules developed and tested in my Splunk homelab.

## Failed Authentications 
sourcetype="WinEventLog:Security" EventCode="4625" <br>
| stats count as FailedAttempts by Account_Name <br>
| where FailedAttempts >= 5<br>
