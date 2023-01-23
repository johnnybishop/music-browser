<template>
    <button class="btn" @click="onClick()">Search</button>
</template>


<script>
export default {
    name: 'Button',
    methods: {
        onClick() {
            console.log('click');
        }
    }
}

</script>

