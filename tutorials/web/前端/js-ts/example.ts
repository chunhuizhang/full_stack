function add(a: number, b: number): number {
  return a + b;
}

let result = add(5, '10');  // TypeScript 会提示错误，因为 '10' 是一个字符串，不能和数字相加
console.log(result);