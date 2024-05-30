function checkPass(value) {
    var count = 0
    //数字
    if (/\d/.test(value)) count++;
    if (/[a-z]/) count++;
    if (/[A-Z]/) count++;
    if (/_/) count++;
    return count >= 2;
}



export {
    checkPass,
}