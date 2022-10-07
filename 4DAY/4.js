function evenSum(array){
    let sum = 0;
    for(let i = 0;i<array.length;i++){
        if(array[i]%2 == 0){
            sum += array[i]
        }
    }
    return sum
}

let numbers = [10,21,30]
let result = evenSum(numbers)
console.log(result)