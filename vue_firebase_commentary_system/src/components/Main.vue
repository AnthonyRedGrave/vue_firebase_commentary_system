<template>
  <div class="main_commentary" v-if="comments.length">
    <div class="userMain">
      <p>Вы вошли как {{username}}</p>
      <router-link to="/logout">Logout</router-link>
    </div>
    <form class="create_new_comment_form" @submit.prevent="createNewAnswer()">
        <textarea placeholder="Комментарий" id="create_new_comment_input" class="form-control create_new_comment_input"></textarea>
        <input type="submit" value="Написать комментарий" class="btn btn-primary create_new_comment_button">
      </form>
      <div class="commentary" v-for="com in comments" :key="com.id">
        <div class="commentary_el">
          <div class="comment_info">
            <div class="comment_user">
              {{com.user_name}}
            </div>
            <div class="comment_text">
              {{com.content}}
            </div>
          </div>
          <div class="comment_actions">
            <input type="submit" value="Ответить" @click="answer_comment(com.id, com.user_name)" class="btn btn-primary answer_comment_button">
            <input type="submit" value="Удалить" @click="delete_comment(com.id)" class="btn btn-danger delete_comment_button">
             
          </div>
          
        </div>
        <form class="form" v-bind:name=com.id v-bind:style="{ display: display }" @submit.prevent="createNewAnswer(com.id)">
          <textarea placeholder="Комментарий" v-bind:id="com.id" class="form-control answer_comment_input"></textarea>
          <input type="submit" value="Ответить на комментарий" class="btn btn-primary post_answer_comment_button">
        </form>
        <div class="hr">
          <hr>
        </div>
        <div class="answers_list" v-if="com.answers">
          <div class="answers"  v-for="ans in com.answers" :key="ans.id">
          <answer :answer_data="ans"/>
          
        </div>
        </div>
        
      </div>
  </div>
  <div class="main_commentary_none" v-else>
    <h3>Пока нет ни одного комментария, но вы можете добавить новый</h3>
    <div class="userMain">
      <p>Вы вошли как {{username}}</p>
    </div>
    <form class="create_new_comment_form" @submit.prevent="createNewAnswer()">
        <textarea placeholder="Комментарий" id="create_new_comment_input" class="form-control create_new_comment_input"></textarea>
        <input type="submit" value="Написать комментарий" class="btn btn-primary create_new_comment_button">
      </form>
    
  </div>
</template>

<script>
import Answer from './Answer.vue'
import axios from 'axios'
import {mapState} from 'vuex'
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
        socket: null,
        comments: [],
        display: 'none',
        comment: {}
      }
    },
    created(){ // при создании компонента запускается подключение к сокету и здесь вылавливаются все сообщения от бэкенда
      this.socket = new WebSocket(
        'ws://'+
        'localhost:8000' +
        '/ws/comments/'
    )
    this.socket.onopen = function(){

    }
    let _this = this
    this.socket.onmessage = function(event){
      let data = JSON.parse(event.data)
      console.log(data)
      if(data.to_delete == 'true'){
        let id_to_delete = data.id
        let result = _this.comments.find(item => item.id == id_to_delete)
        console.log(result)
        let indexRes = _this.comments.indexOf(result)
        _this.comments.splice(indexRes, 1)
      }
      else if (data.parent == null){
        _this.comments.push(data)
      }
      else{
        let id = data.parent
        let result = _this.comments.find(item => item.id == id)
        if ("answers" in result){
          result.answers.push(data)
        }
        else{
          result.answers = []
          result.answers.push(data)
        }
      }
    }
      
    },
    mounted(){
      this.get_comment_list()
    },
    
    computed: mapState(['APIData', 'username']),
    
    
    methods:{
      get_comment_list(){ // получение данных апи от бэкенда в json
      console.log(this.$store.state.accessToken)
        axios.get('http://localhost:8000/api/comments/list/', {headers:{Authorization: `Bearer ${this.$store.state.accessToken}`}})
        .then(responce=>{
          console.log("зашел")

          this.$store.state.APIData = responce.data
          this.comments=responce.data
          console.log(responce.data)
          })
        .catch(err=>{
          console.log(err)
        })
      },
      answer_comment(id, username_to){ // функция отвечаюшая за отображение формы ввода ответа пользователя для выбранного комментария
        const list = document.querySelectorAll('.form')
        for(let i=0;i<list.length;i++){
          list[i].style.display = 'none'
        }
        
        const create_answer_form = document.getElementsByName(id); // форма с ответом и айди родителя
        create_answer_form[0][0].value = username_to + ','
        create_answer_form[0].style.display = 'block' // сделать только его видимым
        
      },
      delete_comment(id){ // удаление комментария
        axios({
            method: 'delete',
            url: 'http://localhost:8000/api/comments/list/' + id + '/',
          }).then(()=>{
            let result = this.comments.find(item => item.id == id) // комментарий, который нужно удалить
            console.log(result)
            this.socket.send(JSON.stringify({
              'parent': null,
              'content': result.content,
              'id': id,
              'date_published': result.date_published,
              'to_delete': 'true'
            }))
            // let indexRes = this.comments.indexOf(result)
            // this.comments.splice(indexRes, 1)
          })
      },
      createNewAnswer(id=null){ // создание либо нового комментария либо нового ответа для комментария
        let new_com_answer_id = null
        let new_com_answer_date_published = null
        if (id==null){
          console.log("создаю новый коммент")
          console.log(this.username)
          let create_new_comment_text = document.getElementById("create_new_comment_input")
          axios({
            method: 'post',
            url: 'http://localhost:8000/api/answers/list/',
            data: {
              content: create_new_comment_text.value,
              parent: id,
              user_name: this.username,
            }
          }).then((responce)=>{
            new_com_answer_id = responce.data.id
            new_com_answer_date_published = responce.data.date_published
            this.socket.send(JSON.stringify({
              'parent': id,
              'user_name': this.username,
              'content': create_new_comment_text.value,
              'id': new_com_answer_id,
              'date_published': new_com_answer_date_published,
              'to_delete': 'false'
            }))
            create_new_comment_text.value = ''
          })
        }
        else{
          let answer_text_value = document.getElementById(id)
          axios({
            method: 'post',
            url: 'http://localhost:8000/api/answers/list/',
            data: {
              content: answer_text_value.value,
              parent: id,
              user_name: this.username,
            }
          }).then((responce)=>{
            new_com_answer_id = responce.data.id
            new_com_answer_date_published = responce.data.date_published
            

            this.socket.send(JSON.stringify({
            'parent': id,
            'content': answer_text_value.value,
            'id': new_com_answer_id,
            'date_published': new_com_answer_date_published,
            'user_name': this.username,
            'to_delete': 'false'
          }))
            answer_text_value.value = ''
          })
        }
      }
    }
}
</script>

<style scoped>
.create_new_comment_input{
  width: 350px;
  margin-bottom: 20px;
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
  top: 40px;
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
.create_new_comment_button{
  margin-left: 165px;
  margin-bottom: 30px;
}
</style>