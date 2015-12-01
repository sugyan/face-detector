/* global $ */
class Main {
    constructor() {
        var canvas = document.getElementById('canvas');
        this.ctx = canvas.getContext('2d');
    }
    load(url) {
        let img = new Image();
        img.onload = () => {
            this.ctx.drawImage(img, 0, 0);
        };
        img.src = url;
    }
}

$(() => {
    var main = new Main();
    $('#url').submit(() => {
        var url = $('input[name="image_url"]').val();
        if (url) {
            main.load(url);
        }
        return false;
    });
});
