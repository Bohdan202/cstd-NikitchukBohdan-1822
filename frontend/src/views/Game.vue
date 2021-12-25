<template>
  <div>

    <Loader v-if="isLoading" />
    <div v-else>
      {{position}}
      <canvas id="canvas"></canvas>
    </div>
    
  </div>
</template>

<script>
import { mapGetters, mapMutations } from 'vuex';
import Loader from '@/components/Loader';

export default {
  name: 'Game',
  components: { Loader },
  data () {
    return {
      msg: '',
      value: '',
      x: 50,
      y: 50,
      chars: {},
      mouseX: 0,
      mouseY: 0,
      keys: {
        'w': 87,
        's': 83,
        'a': 65,
        'd': 68,
        'f': 70,
        'r': 82,
        'q': 81,
        'e': 69,
        'space': 32,
        'shift': 16,
        '1': 49,
        '2': 50,
        '3': 51,
        '4': 52,
        '5': 53,
        'p': 80,
        'i': 73,
        'k': 75,
        'm': 77
      },
      keyPressed: {},
      move_interval: null,
      draw_interval: null
    }
  },
  watch: {
  },
  methods: {
    ...mapMutations(['changeIsLoading']),
    draw () {
      const chars = this.chars;
      
      const ctx = this.ctx;
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      // let x = this.x;
      // let y = this.y;
      
      Object.values(chars).forEach(char => {
        // console.log('chars:', chars);

        if (!char.image) {
          const img = new Image(32, 32);
          img.src = char.img;
          char.image = img;
        } else {
          ctx.save();
          ctx.beginPath();

          // рисование круглой фигуры
          ctx.arc(char.x, char.y, 16, 0, Math.PI*2, true);
          ctx.closePath();
          // ctx.fill();
          ctx.clip();
      
          // картинка показывается на пересечении самой картинки и фигуры
          // ctx.globalCompositeOperation = 'source-in';

          // добавление картинки в canvas
          ctx.drawImage(char.image, char.x-16, char.y-16, 32, 32)
          ctx.restore();
        }

        ctx.font = "10px Verdana";
        ctx.textAlign = "center";
        ctx.fillText(char.nickname, char.x, char.y-18);
      });
      
      // if (this.nickname) {
      //   ctx.font = "10px Verdana";
      //   ctx.textAlign = "center";
      //   ctx.fillText(this.nickname, x, y-18);
      // }

      //draw line start
      ctx.beginPath();
      ctx.moveTo(this.canvas.width/2, this.canvas.height/2);
      ctx.lineTo(this.mouseX, this.mouseY);
      ctx.stroke();   
      //draw line end

      // console.log("angle:", this.angle*180/Math.PI + 'gr');

    }
  },
  computed: {
    ...mapGetters(['isLoading', 'nickname']),
    canvas() {
      return document.getElementById("canvas")
    },
    ctx() {
      return canvas.getContext("2d")
    },
    angle () {
      let x = this.mouseX;
      let y = this.mouseY;

      let cx = this.canvas.width/2;
      let cy = this.canvas.height/2;

      // console.log("angle:", angle(mouseX, mouseY)*180/Math.PI);
      // console.log("angle:", Math.atan((x-cx)/(y-cy))*180/Math.PI + 'gr');

      return Math.atan((x-cx)/(y-cy));
    },
    position() {
      let position = 'x: ' + Math.round(this.x*100)/100 + ' / y: ' + Math.round(this.y*100)/100;
      return position
    }
  },
  mounted() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight * 94 / 100;

    document.addEventListener('keydown', (event) => {
      const keyPressed = this.keyPressed;

      keyPressed[event.keyCode] = true;

      // this.draw();
    })

    document.addEventListener('keyup', (event) => {
      this.keyPressed[event.keyCode] = false;
    })

    const move = () => {
      const keyPressed = this.keyPressed;
      const key = this.keys;

      let speed = 1;
      let x=0, y=0;

      if (keyPressed[key.a]) x -= speed;
      if (keyPressed[key.d]) x += speed;
      if (keyPressed[key.w]) y -= speed;
      if (keyPressed[key.s]) y += speed;

      if (x || y) {
        const sended_data = { x: x, y: y };
      
        this.$socket.emit('set_position', sended_data);
      }
    }

    this.move_interval = setInterval(move, 10);
    this.draw_interval = setInterval(this.draw, 10);

    document.addEventListener("mousemove", () => {
      let mouseX = event.clientX;
      let mouseY = event.clientY - 6 * this.canvas.height / 100;

      this.mouseX = mouseX;
      this.mouseY = mouseY;

      // console.log("mouse:", mouseX, mouseY);
      // console.log("angle:", angle(mouseX, mouseY)*180/Math.PI);
    });

    window.addEventListener(`resize`, event => {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight * 94 / 100;
    }, false);

    this.sockets.subscribe("update_user", (data) => {
      if (!this.chars[data.id]) {
        this.chars[data.id] = data.user;
      } else {
        for (let key in data.user) {
          if (!this.chars[data.id][key] || data.user[key] != this.chars[data.id][key]) {
            this.chars[data.id][key] = data.user[key];
          }
        }
      }

      this.x = this.chars[this.$cookies.get('uid')].x;
      this.y = this.chars[this.$cookies.get('uid')].y;

      // console.log("chars:", this.chars);
    });

      const sended_data = {};

      this.$http.post('new_player', sended_data, { withCredentials: true })

      .then(response => response.json())
      .then(data => {
        // console.log("new_player", data);
      })
      .catch((err) => {
        console.log("new_player", err);
      });

    // });

  },
  destroyed() {
    this.sockets.unsubscribe("update_user", (data) => {
      this.chars = data.chars;
    });
    
    clearInterval(this.move_interval);
    clearInterval(this.draw_interval);
  }
}
</script>

<style lang="scss" scoped>

#canvas {
  position: fixed;

  // width: 100vw;
  // height: 94vh;

  left: 0;
  bottom: 0;
}

h1, h2 {
  font-weight: normal;
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  display: inline-block;
  margin: 0 10px;
}

a {
  color: #42b983;
}

</style>
