var image = new MarvinImage();
var gray_scale_image = new MarvinImage();

image_file_input.addEventListener("change",(ev)=>{
    console.log(ev);
    console.log();
    if(ev.target.files.length){
        show_black_and_white_image(ev.target.files[0]);
    }
})


function show_black_and_white_image(file){
    var fr = new FileReader();
    fr.onload = ()=>{
        original_img.src = fr.result;

        // var canvas = document.createElement("canvas");
        // var ctx = canvas.getContext("2d");

        // original_img.onload = function() {
        //     console.log(original_img.width,original_img.height);
        //     // console.log(original_img.width,original_img.height);
        //     canvas.height = original_img.height;
        //     canvas.width = original_img.width;
            
        //     ctx.drawImage(original_img, 0, 0,original_img.width,original_img.height);
        //     console.log(canvas.width,canvas.height);
            
        //     // image grayscale logic
        //     var imageData = ctx.getImageData(0,0,original_img.width,original_img.height);

        //     for(var i=0;i<imageData.data.length;i+=4){
        //         var avg = (
        //             imageData.data[i]
        //             + imageData.data[i+1]
        //             + imageData.data[i+2]
        //         )/3;

        //         imageData.data[i] = avg;
        //         imageData.data[i+1] = avg;
        //         imageData.data[i+2] = avg;

        //     }
        //     ctx.putImageData(imageData,0,0,0,0,imageData.width,imageData.height);

        //     original_img.src = canvas.toDataURL();
        //     original_img.onload = null;
        // };

        colorize();
    }
    fr.readAsDataURL(file);
}

function colorize(){
    fetch(original_img.src)
    .then((response)=>{
        return response.blob()
    })
    .then((blob)=>{
        // now send it
        var formdata = new FormData();
        formdata.append("image",blob,"image");
        fetch("/colorize",{
            method:"POST",
            body:formdata,
        })
        .then(res=>res.json())
        .then((data)=>{
            console.log(data);
            result_img.src = "data:image/png;charset=utf-8;base64,"+data["image"];
        })
    })
}