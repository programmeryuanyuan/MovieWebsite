<template>
    <div>
        <button @click="toggleChat" class="btn chat-icon">
            <img :src="isChatOpen ? '/icons/chat.png' : '/icons/sleeping.png'" alt="Chat icon" />
        </button>
        <div v-if="isChatOpen" class="chat-window">
            <div class="chat-header">Chat Bot</div>
            <div class="chat-body">
                <ul>
                    <li v-for="message in messages">{{ message }}</li>
                </ul>
            </div>
            <div class="chat-footer">
                <form @submit.prevent="sendMessage">
                    <input type="text" v-model="inputMessage" class="form-control" placeholder="Type a message...">
                    <button type="submit" class="btn btn-info">Send</button>
                </form>
            </div>
        </div>
    </div>
</template>

<script>
export default {
    name: "chatbot",
    data() {
        return {
            isChatOpen: false,
            inputMessage: '',
            messages: [],
        }
    },
    methods: {
        toggleChat() {
            this.isChatOpen = !this.isChatOpen
        },
        sendMessage() {
            // 在这里发送消息到聊天机器人
            this.messages.push(this.inputMessage)
            this.inputMessage = ''
        }
    }
}
</script>

<style scoped>
.chat-icon {
    position: fixed;
    bottom: 32px;
    right: 32px;
    z-index: 9999;
}

.chat-icon img {
    width: 100%;
    height: 100%;
}


.chat-window {
    position: fixed;
    bottom: 80px;
    right: 20px;
    width: 300px;
    height: 400px;
    border: 1px solid #ddd;
    z-index: 9999;
}

.chat-header {
    background-color: #f0f0f0;
    padding: 10px;
    font-weight: bold;
    text-align: center;
}

.chat-body {
    background-color: #ffffff;
    height: 300px;
    overflow-y: scroll;
    padding: 10px;
}

.chat-footer {
    padding: 10px;
    background-color: #f0f0f0;
    border-top: 1px solid #ddd;
}

.chat-footer form {
    display: flex;
    align-items: center;
}

.chat-footer input[type="text"] {
    flex: 1;
    margin-right: 10px;
}
</style>
