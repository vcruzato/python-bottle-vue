new Vue({
    delimiters: ['${', '}'],
    el: '#registerCustomer',
    data: {
        message: '',
        customer: '',
        customerList: '',
        customerSelected: '',        
        riskType: '',
        riskSelected: '',
        riskTypeList: '',
        riskField: '',
        riskFieldList: '',
        fieldSelected: '',
        fieldValue: '',
        fieldValueList: ''
    },
    methods: {
        getCustomer: function () {
            this.$http.get('/getCustomer').then(function(response) {
                this.customerList = response.data.getCustomer;
            })
        },
        addCustomer: function () {
            this.$http.post('/addCustomer',{'customer': this.customer}).then(response => {
                if (response.data.status) {
                    this.message = '';
                    this.customer = '';
                    this.getCustomer();
                } else {
                    this.message = response.data.error;
                }
            }, response => {
                console.log('addCustomer Error:' + response.data);
            });
        },
        getType: function () {
            this.riskTypeList = '';
            this.riskSelected = '';
            this.riskFieldList = '';
            this.fieldSelected = '';
            this.fieldValue = '';
            this.fieldValueList = '';
            this.$http.get('/getType?customer='+this.customerSelected).then(function(response) {
                if (response.data.getType.length) {
                    this.riskTypeList = response.data.getType;
                }
            })
        },
        addType: function () {
            param = {'customer': this.customerSelected, 'type': this.riskType}
            this.$http.post('/addType', param).then(response => {
                if (response.data.status) {
                     this.riskType = '';
                    this.getType();
                } else {
                    this.message = response.data.error;
                }
            }, response => {
                console.log('addType Error:' + response.data)
            });
        },
        getField: function () {
            this.riskFieldList = '';
            this.$http.get('/getField?customer='+this.customerSelected +'&type='+this.riskSelected).then(function(response) {
                if (response.data.getType.length) {
                    this.riskFieldList = response.data.getType;
                }
            })
        },
        addField: function () {
            param = {'customer': this.customerSelected,
                     'type': this.riskSelected,
                     'field': this.riskField}
            this.$http.post('/addField', param).then(response => {
                if (response.data.status) {
                    this.riskField = '';
                    this.getField();
                } else {
                    this.message = response.data.error;
                }
            }, response => {
                console.log('addField Error:' + response.data)
            });

        },
        getValue: function () {
            this.$http.get('/getValue?type='+this.riskSelected).then(function(response) {
                if (response.data.getType.length) {
                    this.fieldValueList = response.data.getType;
                }
            })
        },
        addValue: function () {
            param = {'customer': this.customerSelected,
                     'type': this.riskSelected,
                     'field': this.fieldSelected,
                     'value': this.fieldValue}
            this.$http.post('/addValue', param).then(response => {
                if (response.data.status) {
                    this.fieldValue='';
                    this.getValue();
                } else {
                    this.message = response.data.error;
                }
            }, response => {
                console.log('addValue Error:' + response.data)
            });

        }

    }
});

new Vue({
    delimiters: ['${', '}'],
    el: '#modelResult',
    data: {
        customerList: '',
        customerSelected: '',
        result: ''
    },
    mounted: function() {
        this.$http.get('/getCustomer').then(function(response) {
            this.customerList = response.data.getCustomer;
        })
    },
    methods: {
        getModelResult: function () {
            this.$http.get('/getModelResult?customer='+this.customerSelected).then(function(response) {
                this.result = response.data.data;
            })
        }
    }
});
