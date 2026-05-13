let List="締切は5月4日(月)17:00です。確認の捺印をもらえなかったときは5月7日(木)にもらいに来てください。絶対に遅れることが無いようにしてください。空欄は認めません。また、classroomからレポートの再提出等で個別にメッセージを送ることがあります。必ず確認・返信しなさい。やり方が解らない者は10階職員室に相談に来てください。";
let hozon=[];
let kekka="";
let conect=["は","な","や","が","へ","に","を","、","。"]
let rdm=1;
let conectrandom=0;
function ma(){
    for(let i=0;i<List.length;i=i+rdm){
        rdm=Math.floor(Math.random()*(List.length/10)+1)
        conectrandom=Math.random()
        if(conectrandom<0.8){
            hozon.push(List.slice(i,i+rdm));
        }
    }
    const f=hozon.length-Math.floor(Math.random()*hozon.length)
    for(let a=0;a<f;a++){
        let random=Math.floor(Math.random()*hozon.length)
        conectrandom=Math.random()
        kekka=kekka+hozon[random]
        if(conectrandom>0.8){
            if(a != hozon.length){
                conectrandom=Math.random()
                conectrandom=Math.floor(conectrandom*conect.length)
                kekka=kekka+conect[conectrandom]
            }
        }
        hozon.splice(random,1)
    }
    console.log(kekka)
}
ma()
