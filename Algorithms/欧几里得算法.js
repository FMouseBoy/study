//功能：求两个数的最大公约数
//参数：两个数：
//返回值：最大公约数

// 递归
function gcb(a,b) {
    let max = a > b?a:b;
    let min = a > b?b:a;
    let r = max % min;
    if(r == 0){
        return min;
    }else {
        return gcb(min,r);
    }
}

let result = gcb(3,9);
console.log(result);
// 简化表达
// function gcb (a,b) {
//     return b===0?a:gcb(b,a%b);
// }

// 循环


function gcb(m,n){
    //1、求最小数
    var min = m<n?m:n;
    //2、从大到小循环找第一个公约数
    for(var i=min;i>=2;i--){
        if(m%i==0 && n%i==0){
            return i;
        }
    }
    return 1;
}
