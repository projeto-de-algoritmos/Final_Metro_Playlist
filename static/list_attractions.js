var selectAttractionModal = document.getElementById('selectAttractionModal')
selectAttractionModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = selectAttractionModal.querySelector('.modal-title')

    var modalContent = selectAttractionModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('confirm')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Selecionar atração ' + attraction_name
    modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + '?'
})

var removeAttractionModal = document.getElementById('removeAttractionModal')
    removeAttractionModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = removeAttractionModal.querySelector('.modal-title')

    var modalContent = removeAttractionModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('cancel')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Remover atração ' + attraction_name
    modalContent.textContent = 'Deseja remover a atração ' + attraction_name + '?'
})


var SelectAttractionOriginModal = document.getElementById('SelectAttractionOriginModal')
    SelectAttractionOriginModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = SelectAttractionOriginModal.querySelector('.modal-title')

    var modalContent = SelectAttractionOriginModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('confirm-origin')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Selecionar atração ' + attraction_name + ' como origem'
    modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + ' como origem?'
})

var RemoveAttractionOriginModal = document.getElementById('RemoveAttractionOriginModal')
    RemoveAttractionOriginModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = RemoveAttractionOriginModal.querySelector('.modal-title')

    var modalContent = RemoveAttractionOriginModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('cancel-origin')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Selecionar atração ' + attraction_name + ' como origem'
    modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + ' como origem?'
})


var SelectAttractionDestinationModal = document.getElementById('SelectAttractionDestinationModal')
    SelectAttractionDestinationModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = SelectAttractionDestinationModal.querySelector('.modal-title')

    var modalContent = SelectAttractionDestinationModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('confirm-destination')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Selecionar atração ' + attraction_name + ' como destino'
    modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + ' como destino?'
})

var RemoveAttractionDestinationModal = document.getElementById('RemoveAttractionDestinationModal')
    RemoveAttractionDestinationModal.addEventListener('show.bs.modal', function (event) {
    // Button that triggered the modal
    var button = event.relatedTarget
    // Extract info from data-bs-* attributes
    var attraction_id = button.getAttribute('data-bs-attraction-id')
    var attraction_name = button.getAttribute('data-bs-attraction-name')
    var modalTitle = RemoveAttractionDestinationModal.querySelector('.modal-title')

    var modalContent = RemoveAttractionDestinationModal.querySelector('.modal-body')

    var confirmButton = document.getElementsByClassName('cancel-destination')
    confirmButton[0].setAttribute('id', attraction_id)

    modalTitle.textContent = 'Selecionar atração ' + attraction_name + ' como destino'
    modalContent.textContent = 'Deseja selecionar a atração ' + attraction_name + ' como destino?'
})


$('.confirm').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/select/' + attraction_id
});

$('.cancel').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/remove/' + attraction_id
});

$('.confirm-origin').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/select-origin/' + attraction_id
});

$('.cancel-origin').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/remove-origin/' + attraction_id
});

$('.confirm-destination').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/select-destination/' + attraction_id
});

$('.cancel-destination').click(function() {
    var attraction_id = $(this).attr('id');
    window.location = '/attractions/remove-destination/' + attraction_id
});
