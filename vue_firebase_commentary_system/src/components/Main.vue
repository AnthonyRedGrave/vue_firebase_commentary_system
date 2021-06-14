<template>
  <div class="main_commentary" v-if="comments.length">
      <input type="text" placeholder="Комментарий" class="form-control commentary_text_input">
      <div class="commentary" v-for="com in comments" :key="com.id">
        <div class="commentary_el">
          <div class="comment_info">
            <div class="comment_user">
              Имя
            </div>
            <div class="comment_text">
              {{com.content}}
            </div>
          </div>
          <div class="comment_actions">
            <input type="submit" value="Ответить" @click="answer_comment(com.id)" class="btn btn-primary answer_comment_button">
            <input type="submit" value="Удалить" @click="delete_comment" class="btn btn-danger delete_comment_button">
             
          </div>
          
        </div>
        <form class="form" v-bind:name=com.id v-bind:style="{ display: display }" @submit.prevent="createNewAnswer(com.id)">
          <textarea placeholder="Комментарий" v-bind:id="com.id" class="form-control answer_comment_input"></textarea>
          <input type="submit" value="Ответить на комментарий" class="btn btn-primary post_answer_comment_button">
        </form>
        <div class="hr">
          <hr>
        </div>
        
        <div class="answers" v-for="ans in com.answers" :key="ans.id">
          <answer :answer_data="ans"/>
          
        </div>
      </div>
  </div>
  <div class="main_commentary_none" v-else>
    <h3>Пока нет ни одного комментария, но вы можете добавить новый</h3>
    <input type="text" v-model="text" class="form-control commentary_text_input">
    
  </div>
</template>

<script>
import Answer from './Answer.vue'
import axios from 'axios'
export default {
    name: 'main',
    components:
    {
      Answer
    },
    props:{

    },
    data(){
      return {
        comments: [],
        display: 'none',
        comment: {}
      }
    },
    mounted(){
      axios.get('http://localhost:8000/api/comments/list/').then(responce=>(this.comments=responce.data))
    },
    
    methods:{
      answer_comment(id){
        const list = document.querySelectorAll('form')
        for(let i=0;i<list.length;i++){
          list[i].style.display = 'none'
        }
        const create_answer_form = document.getElementsByName(id); // форма с ответом и айди родителя
        create_answer_form[0].style.display = 'block' // сделать только его видимым
        
      },
      delete_comment(){
        console.log("delete на коммент")
      },
      createNewAnswer(id){
        let answer_text_value = document.getElementById(id)
        axios({
          method: 'post',
          url: 'http://localhost:8000/api/answers/list/',
          data: {
            content: answer_text_value.value,
            parent: id
          }
        }).then((responce)=>{
          this.comments.push(responce.data)
          console.log(responce.data)
          answer_text_value = ''
        })
        
      }
    }
    // created(){
    //   let username = prompt("Введите свое имя")
    //   this.username = username
    // }
}
</script>

<style scoped>
.commentary_text_input{
  width: 350px;
  margin-bottom: 30px;
  margin-top: 30px;
  margin-left: 20px;
}

.commentary_el{
  margin-bottom: 10px;
  width: 250px;
  min-height: 150px;
  background-color: #ef3038;
  border-radius: 10px;
  margin-left: 20px;
}

.comment_info{
  position: relative;
  left: 20px;
}
.comment_user{
  border-bottom: 1px solid black;
  width: 220px;
}
.comment_actions{
  position: relative;
  top: 60px;
  left: 60px;
}
.hr{
  width: 470px;
  left: 20px;
  position: relative;
}
.answers{
  margin-top: 10px;
  
  width: 570px;
  left: 50px;
  position: relative;
}

.answer_comment_input{
  width: 380px;
  margin-left: 35px;
}

.post_answer_comment_button{
  margin-left: 185px;
  margin-top: 15px;
}
</style>