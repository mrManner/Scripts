<#  Takes a file with email adresses, a text file, and possibly some
    other file(s) and emails it all using Outlook. (It's silly, I know.)

    The text file should have the email subject on the first line, followed by 
    exactly two blank lines, and then the email body.

    The list of email adresses can have one or several emails per row. Each row 
    corresponds to one email. Multiple emails on a row should be 
    semicolon-separated.
#>

param([string]$to, [string]$text, [string]$attachment)

function FullPath([string]$path) {
    [System.IO.Path]::GetFullPath((Join-Path (pwd) $path))
}

function SendMail([string]$subject, [System.Array]$text, [string]$attachment, [string]$to) {
    $outlook = New-Object -com Outlook.Application

    # Sends a single email using the provided outlook session
    
    $mail = $outlook.CreateItem(0)
    $mail.Subject = $subject
    $mail.Body = $text[3..($text.Length-1)]
    [void]$mail.Attachments.Add($attachment)
    $mail.To = $to
    $mail.Send()
    #>
}

#Start-Process Outlook

$textrows = (Get-Content (FullPath $text))
$subject = $textrows[0]
$body = $textrows[3..($textrows.Length-1)] -join "`n"
(Get-Content (FullPath($to))) | ForEach-Object {
   sendmail $subject $body (FullPath $attachment) $_
   Start-Sleep -m 250 
}
