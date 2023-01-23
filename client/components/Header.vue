<template>
    <header>
        <h1>{{ title }}</h1>
    </header>
</template>

<script>

export default {
    name: 'Header',
    props: {
        title: {
            type: String,
            default: 'Music browser'
        }
    },
    components:{    }
}
</script>

<style scoped>
header {
    display:flex;
    justify-content: center;
    align-items: center;
    margin-bottom: 10px;
}

</style>