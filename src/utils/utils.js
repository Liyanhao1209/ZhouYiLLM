function formatDateTime(isoString) {  
    // 解析ISO 8601格式的日期时间字符串  
    const date = new Date(isoString);  
  
    // 提取月和日（注意JavaScript中月份是从0开始的，所以需要+1）  
    const month = String(date.getMonth() + 1).padStart(2, '0');  
    const day = String(date.getDate()).padStart(2, '0');  
  
    // 提取小时和分钟  
    const hours = String(date.getHours()).padStart(2, '0');  
    const minutes = String(date.getMinutes()).padStart(2, '0');  
  
    // 拼接成你想要的格式  
    return `${month}-${day} ${hours}：${minutes}`;  
}  
  
export{
    formatDateTime
}

// 使用函数  
