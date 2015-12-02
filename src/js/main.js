/* global $ */
class Main {
    constructor(canvas, output) {
        this.output = $(output);
        this.width  = canvas.width;
        this.height = canvas.height;
        this.ctx = canvas.getContext('2d');
    }
    load(url) {
        const img = new Image();
        img.onload = () => {
            const scale = Math.max(img.width  / this.width, img.height / this.height);
            const w = img.width  / scale;
            const h = img.height / scale;
            const offset_x = (this.width - w) / 2.0;
            const offset_y = (this.width - h) / 2.0;
            this.fillStyle = 'rgb(0, 0, 0)';
            this.ctx.fillRect(0, 0, this.width, this.height);
            this.ctx.drawImage(img, offset_x, offset_y, w, h);
            this.output.text('');
            $.ajax({
                url: '/api',
                data: {
                    url: url
                },
                success: (result) => {
                    this.output.text(JSON.stringify(result, null, '  '));
                    result.faces.forEach((face) => {
                        const center = {
                            x: offset_x + face.center.x * w / 100.0,
                            y: offset_y + face.center.y * h / 100.0
                        };
                        const rad = Math.atan2((face.eyes[0].y - face.eyes[1].y) * h, (face.eyes[0].x - face.eyes[1].x) * w);
                        const tl = this.rotate({ x: offset_x + (face.center.x - face.w * 0.5) * w / 100.0, y: offset_y + (face.center.y - face.h * 0.5) * h / 100.0 }, center, -rad);
                        const tr = this.rotate({ x: offset_x + (face.center.x + face.w * 0.5) * w / 100.0, y: offset_y + (face.center.y - face.h * 0.5) * h / 100.0 }, center, -rad);
                        const bl = this.rotate({ x: offset_x + (face.center.x - face.w * 0.5) * w / 100.0, y: offset_y + (face.center.y + face.h * 0.5) * h / 100.0 }, center, -rad);
                        const br = this.rotate({ x: offset_x + (face.center.x + face.w * 0.5) * w / 100.0, y: offset_y + (face.center.y + face.h * 0.5) * h / 100.0 }, center, -rad);
                        // draw face rectangle
                        this.ctx.beginPath();
                        this.ctx.moveTo(tl.x, tl.y);
                        this.ctx.lineTo(tr.x, tr.y);
                        this.ctx.lineTo(br.x, br.y);
                        this.ctx.lineTo(bl.x, bl.y);
                        this.ctx.closePath();
                        this.ctx.lineWidth = 2;
                        this.ctx.strokeStyle = 'rgb(0, 255, 0)';
                        this.ctx.stroke();
                        // draw eye
                        face.eyes.forEach((eye) => {
                            this.ctx.beginPath();
                            this.ctx.arc(
                                offset_x + eye.x * w / 100.0,
                                offset_y + eye.y * h / 100.0,
                                (face.w + face.h) / 10.0,
                                0.0, Math.PI * 2.0
                            );
                            this.ctx.lineWidth = 2;
                            this.ctx.strokeStyle = 'rgb(255, 0, 0)';
                            this.ctx.stroke();
                        });
                    });
                }
            });
        };
        img.src = url;
    }
    rotate(target, center, rad) {
        return {
            x:   Math.cos(rad) * target.x + Math.sin(rad) * target.y - center.x * Math.cos(rad) - center.y * Math.sin(rad) + center.x,
            y: - Math.sin(rad) * target.x + Math.cos(rad) * target.y + center.x * Math.sin(rad) - center.y * Math.cos(rad) + center.y
        };
    }
}

$(() => {
    const main = new Main(
        document.getElementById('canvas'),
        document.getElementById('response')
    );
    $('#url').submit(() => {
        const url = $('input[name="image_url"]').val();
        if (url) {
            main.load(url);
        }
        return false;
    });
});
