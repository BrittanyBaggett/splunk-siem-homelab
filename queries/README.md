
## Authentications

**Successful Authentications**<br>
index=main sourcetype="WinEventLog:Security" EventCode=4624 <br>
| table EventCode, LogName, ComputerName, Account_Name, Logon_Process
| sort -_time<br>

**Failed Authentications**<br>
index=main sourcetype="WinEventLog:Security" EventCode=4625<br>
| table _time,ComputerName, EventCode, Account_Name<br>
| sort -_time<br>

