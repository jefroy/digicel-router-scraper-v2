# Hide PowerShell window
Add-Type -Name Window -Namespace Console -MemberDefinition '
[DllImport("Kernel32.dll")]
public static extern IntPtr GetConsoleWindow();

[DllImport("user32.dll")]
public static extern bool ShowWindow(IntPtr hWnd, Int32 nCmdShow);
'
$consolePtr = [Console.Window]::GetConsoleWindow()
# 0 = hide, 5 = show
[Console.Window]::ShowWindow($consolePtr, 0)

# Loop to run the Python script every 5 minutes
while ($true) {
    # Specify the path to your Python script
    $pythonScript = "main.py"

    # Print start message
    $currentDate = Get-Date
    Write-Output "Running the Python script at $currentDate"

    # Run the Python script
    Start-Process "python" -ArgumentList "$pythonScript" -NoNewWindow -Wait

    # Print completion message
    Write-Output "Python script completed at $(Get-Date)"

    # Initialize countdown for next run
    $countdownTime = 300  # 300 seconds = 5 minutes
    while ($countdownTime -gt 0) {
        Write-Output "Next run in $countdownTime seconds..."
        Start-Sleep -Seconds 1
        $countdownTime--
    }
}
