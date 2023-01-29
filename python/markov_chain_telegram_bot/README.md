# Markov chain telegram bot

Для использования в файл `text.txt` скопировать результат со страницы 
экспортированной переписки телеграмма.

```js
console.log(Array.prototype.slice.call(document.querySelectorAll('.text'))
    .filter((_,i)=>i!=0).map(e=>{return e.innerHTML})
    .map(e=>{return e.trim()})
    .reduce((p,c)=>{ return p+'\n'+c}))
```