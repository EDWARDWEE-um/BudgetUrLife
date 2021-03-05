(function(){
    console.log('hym')
    document.querySelector('#categoryInput').addEventListener('keydown', function(e){
    console.log('hi')
      if (e.keyCode != 13){
        return;
      }
  
      e.preventDefault()
  
      var categoryName = this.value
      this.value = ''
      
      addNewCategory(categoryName)
      updateCategoriesString()
    })
  
    function addNewCategory(name){
  
      document.querySelector('#categoriesContainer').insertAdjacentHTML('beforeend',
      `<li class="category">
        <span class="name">${name}</span>
        <span onclick="removeCategory(this)" class="btnRemove bold">X</span>
      </li>`)
    }
  
  })()
  
  function fetchCategoryArray(){
    var categories = []
  
    document.querySelectorAll('.category').forEach(function(e){
      name = e.querySelector('.name').innerHTML
      if (name == '') return
  
      categories.push(name)
    })
  
    return categories
  }
  function fetchCategoryArray(){
    var categories = []
  
    document.querySelectorAll('.category2').forEach(function(e){
      name = e.querySelector('.name').innerHTML
      if (name == '') return
  
      categories.push(name)
    })
  
    return categories
  }
  
  function updateCategoriesString(){
    categories = fetchCategoryArray()
    document.querySelector('input[name="categoriesString"]').value = categories.join(',')
  }
  
  function removeCategory(e){
    e.parentElement.remove()
    updateCategoriesString()
  }

  