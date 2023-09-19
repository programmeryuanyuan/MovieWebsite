
<template>
    
    <button class="floating-btn"
    :style="{ bottom: `${y}px`, right: `${x}px` }"
    @mousedown="handleMouseDown"
    @mousemove="handleMouseMove"
    @mouseup="handleMouseUp"
    @mouseleave="handleMouseLeave"
    @mouseclick="handleClick"
    >
      <slot></slot>
      
    </button>
    <Dialog v-if="dialogVisible" id="dialog-container"
    
    
      title="My Dialog"
      @close="dialogVisible = false"></Dialog>
  </template>
  <script>
import Dialog from './dialog.vue';
  export default {
    components:{
        Dialog,
    },
    data() {
      return {
        x: 20,
        y: 20,
        isDragging: false,
        initialMouseX: 0,
        initialMouseY: 0,
        initialX: 0,
        initialY: 0,
        dialogVisible:false,
        firstTime:0,
        lastTime:0,
        bounds:null,
        displaystyle:"none"
      };
    },
    methods: {
        mounted() {
            this.bounds = this.$refs.dialog.getBoundingClientRect();
        },
        updated() {
            this.bounds = this.$refs.dialog.getBoundingClientRect();
        },

        
      handleMouseDown(event) {
        console.log("down");
        this.firstTime=new Date().getTime();
        this.isDragging = true;
        this.initialMouseX = event.clientX;
        this.initialMouseY = event.clientY;
        this.initialX = this.x;
        this.initialY = this.y;
      },
      handleMouseMove(event) {
        if (this.isDragging) {
          const deltaX = event.clientX - this.initialMouseX;
          const deltaY = event.clientY - this.initialMouseY;
          this.x = this.initialX - deltaX;
          this.y = this.initialY - deltaY;
        }
      },
      handleMouseUp() {
        //lastTime=
        if((new Date().getTime()-this.firstTime<200)){
            this.dialogVisible = true;
            console.log("click");
            const element = document.getElementById("dialog-container");
            if (element.style.display === "none") {
                element.style.display = "block";
            } else {
                element.style.display = "none";
            }
        }
        this.isDragging = false;
      },
      handleMouseLeave(event){
        if(this.bounds && (event.clientX < this.bounds.left  ||
          event.clientX > this.bounds.right  ||
          event.clientY < this.bounds.top  ||
          event.clientY > this.bounds.bottom )
      ){
        this.isDragging=false;
      }
      }
    },
  };
  </script>
  <style>
  .floating-btn {
    position: fixed;
    bottom: 20px;
    right: 20px;
    box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.25);
    background-color: #ff5722;
    color: #fff;
    border: none;
    border-radius: 50%;
    height: 60px;
    width: 60px;
    font-size: 24px;
    line-height: 60px;
    text-align: center;
    cursor: pointer;
    z-index: 9999;
  }
  </style>
  
  