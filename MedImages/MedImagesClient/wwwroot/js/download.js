window.blazorDownloadFile = (filename, exportUrl) => {
    const a = document.createElement("a");
    a.href = exportUrl;
    a.download = filename;
    a.click();
    a.remove();
}