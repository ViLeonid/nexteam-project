<template>
    <div class="confirm-toast">

        <div class="text">
            {{ message }}
        </div>

        <div class="actions">

            <button
                class="confirm"
                @click="confirm"
            >
                Удалить
            </button>

            <button
                class="cancel"
                @click="cancel"
            >
                Отмена
            </button>

        </div>

    </div>
</template>


<script setup>

const props = defineProps({
    message: {
        type: String,
        default: "Удалить?"
    },

    onConfirm: Function,
    onCancel: Function
})


function confirm(){
    props.onConfirm?.()
}


function cancel(){
    props.onCancel?.()
}

</script>


<style scoped>

.confirm-toast {
    display:flex;
    flex-direction:column;
    gap:15px;
}


.text {
    color:white;
    font-size:15px;
}


.actions {
    display:flex;
    gap:10px;
}


.actions button {

    border:none;
    border-radius:10px;

    padding:8px 16px;

    cursor:pointer;

    font-weight:600;

    transition:.2s ease;
}


.confirm {

    background:white;
    color:black;

}


.confirm:hover {

    box-shadow:
        0 0 15px rgba(255,255,255,.5);

}


.cancel {

    background:#181818;
    color:#aaa;

}


.cancel:hover {

    color:white;

}

</style>