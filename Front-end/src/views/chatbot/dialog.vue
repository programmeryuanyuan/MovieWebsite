<template>
    
    <div class="chat-container">
        <div class="message" v-for="(message, index) in messages" :key="index" :class="{ 'my-message': message.isMine, 'their-message': !message.isMine }">
        <div class="bubble">{{ message.content }}</div>
        </div>
        <div class="input-container">
            <input v-model="userInput" placeholder="Type your message here..." />
            <button @click="submitQuestion">send</button>
        </div>
    </div>

    
  </template>
  
  <script>
  import axios from "axios";
  import { useStore } from 'vuex'
  import { watchEffect } from 'vue';
  import { ref } from 'vue';
  export default {
    name: 'Dialog',
    data() {
      return {
        userInput: "",
        answer: "",
        achievements: "",
        context: "context:",
        messages: [{ content: "Hello! I'm your AI Movie Assistant. I provide movie recommendations, information, and reviews to enhance your movie experience. Feel free to ask me any movie questions!", isMine: false}],
      };
    },
    methods: {
      
      async submitQuestion() {
        console.log(this.userInput)
        if (this.userInput.trim() === "") return;
        this.messages.push({ content: this.userInput, isMine: true });
        this.context=this.context+this.userInput+"  ";
        const chatContainer = document.querySelector('.chat-container');
        chatContainer.scrollTop = chatContainer.scrollHeight;
        try {
          const response = await axios.post("http://localhost:5050/get_answer", {
            user_input: this.userInput,
            context:this.context,
            achievements:this.achievements,
          });
          
          this.answer = response.data.answer;
          this.messages.push({ content: this.answer, isMine: false });
          this.context=this.context+this.answer+"  ";
          const chatContainer = document.querySelector('.chat-container');
          chatContainer.scrollTop = chatContainer.scrollHeight;
        } catch (error) {
          console.error(error);
        }
        

        this.userInput = "";
      },
    },
    setup(){
      const store = useStore();
      const config = {
            headers: {
                'Access-Control-Allow-Origin': '*'
            }
        };
      const getAchievements = async () => {
          const userInfo = store.state.userInfo;
          if (!userInfo.id) return;
          try {
              const response = await axios.get("http://localhost:5050/user/" + userInfo.id + "/achievements",config);
              if (response.data) {
                  console.log("achievements:");
                  
                  achievements.value=response.data;
                  console.log(achievements.value);
                  
              }
          } catch (error) {
              console.error(error);
          }
      };
      const achievements = ref([])
        
      watchEffect(() => {
          getAchievements();
      });

      return {
          achievements,
          
      }
    }
    
  };
  </script>
  <style scoped>

    .chat-container {
    position: fixed;
    bottom: 0;
    right: 0;
    width: 400px;
    height: 500px;
    z-index: 5;
    background-color: #d9e9ff;;
    border-radius: 20px;
  }
  .message {
    display: flex;
    margin-bottom: 10px;
  }
  
  .my-message {
    justify-content: flex-start;
  }
  
  .their-message {
    justify-content: flex-end;
  }
  
  .bubble {
    display: inline-block;
    padding: 10px 20px;
    border-radius: 20px;
    background-color: #ffffff;
    font-size: 14px;
  }
  
  .my-message .bubble {
    background-color: #d9e9ff;
  }
  


.input-container {
  position: sticky;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 10px;
  
  width: 100%;
}

.input-container input {
  flex-grow: 1;
  padding: 5px 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  outline: none;
  font-size: 16px;
}

.input-container button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 5px 15px;
  margin-left: 10px;
  cursor: pointer;
  border-radius: 4px;
  outline: none;
  font-size: 16px;
}

.input-container button:hover {
  background-color: #45a049;
}
.chat-container::-webkit-scrollbar {
  display: none;
}

.chat-container {
  -ms-overflow-style: none;  /* IE 和 Edge */
  scrollbar-width: none;  /* Firefox */
}

  </style>
  
  