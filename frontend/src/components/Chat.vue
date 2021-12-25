<template>
  <div>
    <div
      id="chat-circle"
      :class="{
        btn: true,
        'btn-raised': true,
        hide: isShow,
      }"
      @click="showChat()"
    >
      <div id="chat-overlay"></div>
      <!-- <i class="material-icons">Chat</i> -->
    </div>

    <div
      :class="{
        'chat-box': true,
        hide: !isShow,
      }"
    >
      <div class="chat-box-header">
        <span class="chat-box-toggle" @click="close()">
          <i class="material-icons">close</i></span
        >
      </div>
      <div class="chat-box-body">
        <div class="chat-box-overlay"></div>
        <div class="chat-logs">
          <div
            class="chat-msg"
            v-for="(message, index) in messages"
            :key="index"
          >
            <div class="cm-msg-time">
              {{ message.time }}
            </div>
            <span class="msg-avatar tooltip" v-if="message.photo !== 'server'">
              <img :src="message.photo" alt="" class="chat_photo" />
              <span class="tooltiptext tooltip-bottom">{{ message.name }}</span>
            </span>
            <div class="cm-msg-text">
              {{ message.text }}
            </div>
          </div>
        </div>
      </div>
      <!--chat-log -->
      <div class="chat-input">
        <form>
          <input
            type="text"
            id="chat-input"
            placeholder="Send a message..."
            v-model="input"
            v-if="iflogin"
            autocomplete="off"
          />
          <input
            type="text"
            id="chat-input"
            value="Please, log in."
            disabled
            v-else
          />
          <button
            class="chat-submit"
            id="chat-submit"
            v-if="iflogin"
          >
            <i class="material-icons" @click="send()">send</i>
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
// import Loader from "@/components/Loader";
import { mapGetters, mapMutations } from "vuex";

export default {
  name: "Chat",
  data() {
    return {
      isShow: false,
      input: "",
      messages: [],
      logs: "",
      keyup_listener: null
    };
  },
  props: ["set_songs"],
  methods: {
    ...mapMutations(["changeIsLoading"]),
    toggleDrawer() {
      this.isShow = !this.isShow;
    },
    showChat() {
      this.isShow = true;
    },
    close() {
      this.isShow = false;
    },
    send() {
      const sended_data = { message: this.input };
      // this.$socket.emit("send_message", sended_data);
      this.$http.post('send_message', sended_data, { withCredentials: true })
      .then(response => { return response.json(); })
      .then(data => {
        console.log('sended');
      })
      .catch((err) => {
        console.log(err)
      })

      this.input = '';
    },
  },
  computed: {
    ...mapGetters(["iflogin", "nickname"]),
  },
  mounted() {
    // this.sockets.subscribe("new_message", (data) => {

    //   this.messages.push({
    //     name: data.user.nickname,
    //     photo: data.user.photo,
    //     time: data.time,
    //     text: data.message,
    //   });

    // });

    this.$pusher.subscribe('chat').bind('new_message', (data) => {
      this.messages.push({
        name: data.user.nickname,
        photo: data.user.photo,
        time: data.time,
        text: data.message,
      });
    });

    // this.$socket.emit("join_to_chat", {});

    // this.sockets.subscribe("join_to_chat", (data) => {
      // data.messages.forEach(element => {
      //   this.messages.push({
      //     name: element.user.nickname,
      //     photo: element.user.photo,
      //     time: element.time,
      //     text: element.message,
      //   });
      // });
    // });

    this.$http.post('join_to_chat', {}, { withCredentials: true })
    .then(response => { return response.json(); })
    .then(data => {
      data.messages.forEach(element => {
        this.messages.push({
          name: element.user.nickname,
          photo: element.user.photo,
          time: element.time,
          text: element.message,
        });
      });
    })
    .catch((err) => {
      console.log(err)
    })

    if (!this.keyup_listener) {
      this.keyup_listener = document.addEventListener('keyup', (event) => {
        if (event.keyCode === 13) {
          if (this.isShow) this.send();
          else this.isShow = true;
        };
        if (event.keyCode === 27) {
          this.isShow = false;
        };
      })
      this.keyup_listener = true;

    }

  },
};
</script>

<style lang="scss" scoped>
$bp-largest: 900px; // 1200px = 75em

.pointer {
  cursor: pointer;
}
html,
body {
  background: #efefef;
  height: 100%;
}
#center-text {
  display: flex;
  flex: 1;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100%;
}
#chat-circle {
  position: fixed;
  bottom: 5vmin;
  right: 5vmin;

  // padding: 1rem 1rem 1rem 1rem;

  width: 4rem;
  height: 4rem;
  border-radius: 50%;
  color: white;
  // padding: 28px;
  cursor: pointer;
  box-shadow: 0px 3px 16px 0px rgba(0, 0, 0, 0.6),
    0 3px 1px -2px rgba(0, 0, 0, 0.2), 0 1px 5px 0 rgba(0, 0, 0, 0.12);

  text-align: center;
  vertical-align: middle;

  // background: #5a5eb9;
  background: url("../assets/img/PNG/icons80.png") no-repeat center;
  background-size: 3.2rem;
}

.btn#my-btn {
  background: white;
  padding-top: 13px;
  padding-bottom: 12px;
  border-radius: 45px;
  padding-right: 40px;
  padding-left: 40px;
  color: #5865c3;
}
#chat-overlay {
  background: rgba(255, 255, 255, 0.1);
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border-radius: 50%;
  // display: none;
}

.chat-box {
  // display:none;
  background: #efefef;
  position: fixed;
  right: 3rem;
  bottom: 50px;
  width: 25rem;
  max-width: 85vw;
  max-height: 100vh;
  border-radius: 5px;
  /*   box-shadow: 0px 5px 35px 9px #464a92; */
  box-shadow: 0px 5px 35px 9px #ccc;
}

// .show_chat-box {
//   display: flex;
// }
.hide {
  display: none;
}

.chat-box-toggle {
  float: right;
  margin-right: 15px;
  cursor: pointer;
}
.chat-box-header {
  background: #5a5eb9;
  height: 3rem;
  border-top-left-radius: 5px;
  border-top-right-radius: 5px;
  color: white;
  text-align: center;
  font-size: 1rem;
  padding-top: 17px;
}
.chat-box-body {
  position: relative;
  height: 370px;
  height: auto;
  border: 1px solid #ccc;
  // overflow: hidden;
}
.chat-box-body:after {
  content: "";
  background-image: url("data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iMjAwIiBoZWlnaHQ9IjIwMCIgdmlld0JveD0iMCAwIDIwMCAyMDAiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyI+PGcgdHJhbnNmb3JtPSJ0cmFuc2xhdGUoMTAgOCkiIGZpbGw9Im5vbmUiIGZpbGwtcnVsZT0iZXZlbm9kZCI+PGNpcmNsZSBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIgY3g9IjE3NiIgY3k9IjEyIiByPSI0Ii8+PHBhdGggZD0iTTIwLjUuNWwyMyAxMW0tMjkgODRsLTMuNzkgMTAuMzc3TTI3LjAzNyAxMzEuNGw1Ljg5OCAyLjIwMy0zLjQ2IDUuOTQ3IDYuMDcyIDIuMzkyLTMuOTMzIDUuNzU4bTEyOC43MzMgMzUuMzdsLjY5My05LjMxNiAxMC4yOTIuMDUyLjQxNi05LjIyMiA5LjI3NC4zMzJNLjUgNDguNXM2LjEzMSA2LjQxMyA2Ljg0NyAxNC44MDVjLjcxNSA4LjM5My0yLjUyIDE0LjgwNi0yLjUyIDE0LjgwNk0xMjQuNTU1IDkwcy03LjQ0NCAwLTEzLjY3IDYuMTkyYy02LjIyNyA2LjE5Mi00LjgzOCAxMi4wMTItNC44MzggMTIuMDEybTIuMjQgNjguNjI2cy00LjAyNi05LjAyNS0xOC4xNDUtOS4wMjUtMTguMTQ1IDUuNy0xOC4xNDUgNS43IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIi8+PHBhdGggZD0iTTg1LjcxNiAzNi4xNDZsNS4yNDMtOS41MjFoMTEuMDkzbDUuNDE2IDkuNTIxLTUuNDEgOS4xODVIOTAuOTUzbC01LjIzNy05LjE4NXptNjMuOTA5IDE1LjQ3OWgxMC43NXYxMC43NWgtMTAuNzV6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIvPjxjaXJjbGUgZmlsbD0iIzAwMCIgY3g9IjcxLjUiIGN5PSI3LjUiIHI9IjEuNSIvPjxjaXJjbGUgZmlsbD0iIzAwMCIgY3g9IjE3MC41IiBjeT0iOTUuNSIgcj0iMS41Ii8+PGNpcmNsZSBmaWxsPSIjMDAwIiBjeD0iODEuNSIgY3k9IjEzNC41IiByPSIxLjUiLz48Y2lyY2xlIGZpbGw9IiMwMDAiIGN4PSIxMy41IiBjeT0iMjMuNSIgcj0iMS41Ii8+PHBhdGggZmlsbD0iIzAwMCIgZD0iTTkzIDcxaDN2M2gtM3ptMzMgODRoM3YzaC0zem0tODUgMThoM3YzaC0zeiIvPjxwYXRoIGQ9Ik0zOS4zODQgNTEuMTIybDUuNzU4LTQuNDU0IDYuNDUzIDQuMjA1LTIuMjk0IDcuMzYzaC03Ljc5bC0yLjEyNy03LjExNHpNMTMwLjE5NSA0LjAzbDEzLjgzIDUuMDYyLTEwLjA5IDcuMDQ4LTMuNzQtMTIuMTF6bS04MyA5NWwxNC44MyA1LjQyOS0xMC44MiA3LjU1Ny00LjAxLTEyLjk4N3pNNS4yMTMgMTYxLjQ5NWwxMS4zMjggMjAuODk3TDIuMjY1IDE4MGwyLjk0OC0xOC41MDV6IiBzdHJva2U9IiMwMDAiIHN0cm9rZS13aWR0aD0iMS4yNSIvPjxwYXRoIGQ9Ik0xNDkuMDUgMTI3LjQ2OHMtLjUxIDIuMTgzLjk5NSAzLjM2NmMxLjU2IDEuMjI2IDguNjQyLTEuODk1IDMuOTY3LTcuNzg1LTIuMzY3LTIuNDc3LTYuNS0zLjIyNi05LjMzIDAtNS4yMDggNS45MzYgMCAxNy41MSAxMS42MSAxMy43MyAxMi40NTgtNi4yNTcgNS42MzMtMjEuNjU2LTUuMDczLTIyLjY1NC02LjYwMi0uNjA2LTE0LjA0MyAxLjc1Ni0xNi4xNTcgMTAuMjY4LTEuNzE4IDYuOTIgMS41ODQgMTcuMzg3IDEyLjQ1IDIwLjQ3NiAxMC44NjYgMy4wOSAxOS4zMzEtNC4zMSAxOS4zMzEtNC4zMSIgc3Ryb2tlPSIjMDAwIiBzdHJva2Utd2lkdGg9IjEuMjUiIHN0cm9rZS1saW5lY2FwPSJyb3VuZCIvPjwvZz48L3N2Zz4=");
  opacity: 0.1;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  height: 100%;
  position: absolute;
  z-index: -1;
}
#chat-input {
  background: #f4f7f9;
  width: 100%;
  position: relative;
  height: 47px;
  padding-top: 10px;
  padding-right: 50px;
  padding-bottom: 10px;
  padding-left: 15px;
  border: none;
  resize: none;
  outline: none;
  border: 1px solid #ccc;
  color: #888;
  border-top: none;
  border-bottom-right-radius: 5px;
  border-bottom-left-radius: 5px;
  overflow: hidden;
}
.chat-input > form {
  margin-bottom: 0;
}
#chat-input::-webkit-input-placeholder {
  /* Chrome/Opera/Safari */
  color: #ccc;
}
#chat-input::-moz-placeholder {
  /* Firefox 19+ */
  color: #ccc;
}
#chat-input:-ms-input-placeholder {
  /* IE 10+ */
  color: #ccc;
}
#chat-input:-moz-placeholder {
  /* Firefox 18- */
  color: #ccc;
}
.chat-submit {
  position: absolute;
  bottom: 3px;
  right: 10px;
  background: transparent;
  box-shadow: none;
  border: none;
  border-radius: 50%;
  color: #5a5eb9;
  width: 35px;
  height: 35px;
}
.chat-logs {
  padding: 15px;
  height: 370px;
  overflow-y: scroll;
}

.chat-logs::-webkit-scrollbar-track {
  // -webkit-box-shadow: inset 0 0 6px rgba(0, 0, 0, 0.3);
  background-color: #f5f5f5;
}

.chat-logs::-webkit-scrollbar {
  width: 5px;
  background-color: #f5f5f5;
}

.chat-logs::-webkit-scrollbar-thumb {
  background-color: #5a5eb9;
}

@media only screen and (max-width: 500px) {
  .chat-logs {
    height: 40vh;
  }
}

.chat-msg.user > .msg-avatar img {
  width: 1rem;
  height: 2rem;
  border-radius: 50%;
  float: left;
  // width: 15%;
}
.chat-msg.self > .msg-avatar img {
  width: 2rem;
  height: 2rem;
  border-radius: 50%;
  float: right;
  // width: 15%;
}

.msg-avatar {
  float: left;
  margin-left: 0.5rem;
}

.cm-msg-text {
  background: white;
  padding: 5px 15px 5px 15px;
  color: #666;
  max-width: 75%;
  float: left;
  margin-left: 10px;
  position: relative;
  margin-bottom: 2px;
  border-radius: 30px;
}
.cm-msg-time {
  padding: 5px 0px 5px 0px;
  color: #666;
  max-width: 75%;
  float: left;
  margin-left: 5px;
  position: relative;
  margin-bottom: 2px;
  border-radius: 30px;
}
.chat-msg {
  clear: both;
}
.chat-msg.self > .cm-msg-text {
  float: right;
  margin-right: 10px;
  background: #5a5eb9;
  color: white;
}
.cm-msg-button > ul > li {
  list-style: none;
  float: left;
  width: 50%;
}
.cm-msg-button {
  clear: both;
  margin-bottom: 70px;
}

// .chat_icon {
//   margin: auto;
//   // margin-left: 0.7rem;
//   background: url('../assets/img/PNG/icons82.png') no-repeat center;
//   background-size: contain;

//   // position: fixed;
//   // right: 2.2vh;
//   // top: 1vh;

//   // height: 4vh;
//   // width: 15vh;

//   cursor: pointer;

//   // border-radius: 100px;
//   // border: 2px solid rgb(128, 128, 128);
//   // box-shadow: 0 0 7px #666;
// }

.chat_photo {
  height: 1.5rem;
  width: 1.5rem;

  border-radius: 100px;
  border: 2px solid rgb(128, 128, 128);
  box-shadow: 0 0 7px #666;

  // cursor: pointer;

  //   width: 1rem;
  //   height: 2rem;
  //   border-radius: 50%;
  //   float: left;
  //   // width: 15%;
}

.tooltip {
  position: relative;
  display: inline-block;
  // border-bottom: 1px dotted black;
}

.tooltip .tooltiptext {
  visibility: hidden;
  width: 120px;
  background-color: black;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 5px 0;

  /* Position the tooltip */
  position: absolute;
  z-index: 1;
}

.tooltip-bottom {
  top: 135%;
  left: 50%;
  margin-left: -60px;
}

.tooltip:hover .tooltiptext {
  visibility: visible;
}
</style>