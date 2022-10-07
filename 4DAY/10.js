function avg(array){
    let grade = 0;
    let cnt = 0;
    for(let i = 0; i<array.length; i++){
        if(array[i] >= 90){
            grade += array[i]
            cnt += 1
        }
    }
    return grade / cnt;
}

let grads = [90,82,100,70,80]
let result = avg(grads)
console.log(result)