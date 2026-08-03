$ErrorActionPreference = "Stop"
function Get-CoreMetrics {
    return @{
        "timestamp" = (Get-Date -Format "yyyy-MM-dd HH:mm:ss.fff");
        "hardware_perf" = @{
            "cpu_load_percent" = [Math]::Round((Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average, 1);
            "available_ram_gb" = [Math]::Round((Get-CimInstance Win32_OperatingSystem).FreePhysicalMemory / 1MB, 2)
        }
    } | ConvertTo-Json -Depth 4
}