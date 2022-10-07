function countGrade(array){
    let cnt = 0;
    for(let i = 0; i<array.length; i++){
        if(array[i] >= 90){
            cnt += 1
        }
    }
    return cnt;
}

let grads=[90,82,100,70,80]
let result = countGrade(grads)
console.log(result)