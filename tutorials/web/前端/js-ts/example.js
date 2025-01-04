function add(a, b) {
  return a + b;
}

let result = add(5, '10');  // 这里没有类型错误，JavaScript 会将数字与字符串相加
console.log(result);  // 输出 "510"（字符串拼接）