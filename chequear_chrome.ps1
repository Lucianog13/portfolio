$procs = Get-CimInstance Win32_Process -Filter "name='chrome.exe'"
foreach ($p in $procs) {
    $cmd = $p.CommandLine
    if ($cmd -match 'user-data-dir|remote-debugging') {
        Write-Output ("PID {0}: {1}" -f $p.ProcessId, $cmd.Substring(0, [Math]::Min(220, $cmd.Length)))
    }
}
Write-Output ("Total chrome: " + $procs.Count)
