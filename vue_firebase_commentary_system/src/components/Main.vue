<template>
  <div class="main_commentary" v-if="fake_comms.length">
      <input type="text" placeholder="Комментарий" class="form-control commentary_text_input">
      <div class="commentary" v-for="com in fake_comms" :key="com.text">
        <div class="commentary_el">
          <div class="comment_info">
            <div class="comment_user">
              {{com.username}}
            </div>
            <div class="comment_text">
              {{com.text}}
            </div>
          </div>
          <div class="comment_actions">
            <input type="submit" value="Ответить" @click="answer_comment" class="btn btn-primary answer_comment_button">
            <input type="submit" value="Удалить" @click="delete_comment" class="btn btn-danger delete_comment_button">
             
          </div>
          
        </div>
        <textarea placeholder="Комментарий" v-bind:style="{ display: display }" class="form-control answer_comment_input"></textarea>
        <div class="hr">
          <hr>
        </div>
        
        <div class="answers" v-for="ans in com.answers" :key="ans.text">
          <answer :answer_data="ans"/>
          
        </div>
      </div>
  </div>
  <div class="main_commentary_none" v-else>
    Пока нет ни одного комментария, но вы можете добавить новый
    <input type="text" v-model="text" class="form-control commentary_text_input">
    
  </div>
</template>

<script>
import Answer from './Answer.vue'
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
        text: null,
        commentary: {},
        commentaries:[],
        display: 'none',
        fake_comms:[
          {
            text: "new comment1",
            username: "Jake",
            date_published: "12.10.2021",
            answers:[
              {
                text: "new comment5ans",
                username: "Marya",
                date_published: "13.10.2021",
              },
              {
                text: "new comment5anscomment5anscomment5anscomment5anscomment5ans",
                username: "Marya",
                date_published: "13.10.2021",
              }
            ]
          },
          {
            text: "new comment2",
            username: "Oleg",
            date_published: "12.10.2021"
          },
          {
            text: "new comment3",
            username: "Fire",
            date_published: "12.10.2021"
          },
          {
            text: "nnew comment4",
            username: "Jake",
            date_published: "12.10.2021"
          },
        ],
        username: null
      }
    },
    
    methods:{
      answer_comment(){
        console.log("ответить на коммент")
        this.display = 'block'
      },
      delete_comment(){
        console.log("delete на коммент")
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
</style>