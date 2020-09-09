for /R .\img %%F in (*.webp) do
    start dwebp "%%I" -o "%%I".png 
    pause
