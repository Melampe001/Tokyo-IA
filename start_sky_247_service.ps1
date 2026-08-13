# Rascacielos Digital - 24/7 Background Daemon Wrapper
$coreDir = "E:\TOKYOAPPS_UNIVERSE\01_ACTIVE\NULOGIC_CORE"
$enterpriseUiDir = "$coreDir\SKY_RASCACIELOS\ENTERPRISE_UI"
$port = 65236
$url = "http://localhost:$port/"

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($url)
try {
    $listener.Start()
    while ($listener.IsListening) {
        $context = $listener.GetContext()
        $request = $context.Request
        $response = $context.Response
        
        $localPath = Join-Path $enterpriseUiDir $request.Url.LocalPath.TrimStart('/')
        if ($request.Url.LocalPath -eq '/' -or $request.Url.LocalPath -eq '') {
            $localPath = Join-Path $enterpriseUiDir 'index.html'
        }
        
        if (Test-Path $localPath -PathType Leaf) {
            $content = [System.IO.File]::ReadAllBytes($localPath)
            $response.ContentLength64 = $content.Length
            $response.ContentType = "text/html; charset=utf-8"
            $output = $response.OutputStream
            $output.Write($content, 0, $content.Length)
            $output.Close()
        } else {
            $response.StatusCode = 404
            $response.Close()
        }
    }
}
finally {
    if ($listener.IsListening) { $listener.Stop() }
}