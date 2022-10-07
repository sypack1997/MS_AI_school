function objectSum(numO){
    let total = 0;
    for(let i = 0; i<numO.length;i++){
        if(numO[i]['number'] % 2 == 1){
            total += numO[i]['number']
        }
    }
    return total;
}

let numObject = [{'name':'lee', 'number':22}, {'name':'park', 'number':11}]
let result = objectSum(numObject)
console.log(result)