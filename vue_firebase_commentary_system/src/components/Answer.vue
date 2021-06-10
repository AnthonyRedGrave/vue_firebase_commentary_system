<template>
  <div class="answer">
      <div class="answer_el">
          <div class="answer_info">
            <div class="answer_user">
              {{answer_data.username}}
            </div>
            <div class="answer_text">
              {{answer_data.text}}
            </div>
          </div>
          
        </div>
  </div>
</template>

<script>
export default {
    name: 'Answer',
    props:{
        answer_data:{
            type: Object,
            default: ()=>{},
        }
    },

}
</script>

<style>
    .answer{
        margin-bottom: 30px;
        
    }
    .answer_el{
        margin-bottom: 10px;
        width: 350px;
        word-break: break-all;
        background-color: #ff496c;
        min-height: auto;
        width: 370px;
        max-height: auto;
        border-radius: 10px;
        margin-left: 20px;
    }

    .answer_info{
        padding-left: 20px;
        padding-right: 20px;
    }
    .answer_user{
        border-bottom: 1px solid black;
        width: 330px;
    }
</style>