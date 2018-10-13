/**
 * @license
 * Copyright (c) 2014, 2018, Oracle and/or its affiliates.
 * The Universal Permissive License (UPL), Version 1.0
 */
/*
 * Your dashboard ViewModel code goes here
 */
define(['ojs/ojcore', 'knockout', 'jquery', 'ojs/ojknockout','ojs/ojdatetimepicker', 'ojs/ojselectcombobox',  'ojs/ojinputtext', 'ojs/ojformlayout'],
 function(oj, ko, $) {
  
    function DashboardViewModel() {
      var self = this;
      self.url = "http://localhost:3000/submitModel"
      self.displayOptimal = false;
      //init variables
      self.dummyModels = ko.observableArray([
        // {value: "KNN", model: "K Nearest Neighbors", hyperparams: {K: "3 5 6"} },
        {value: "logisticregression", model: "Logistic Regression", hyperparams: {penalty: "l1 l2", C: "1 1e-2 1e-1 100 10"} },
        {value: "decisiontreeclassifier", model: "Decision Trees", hyperparams: {max_depth: "1 2 3 4 7 9 11 15 20 25 100", criterion: "gini entropy"} },
        {model: "Neural Networks", value: "neuralnetworkclassifier", hyperparams: {hidden_layer_sizes: "10,10 20,10 50,10", activation: "tanh relu", solver : "sgd adam", learning_rate: "constant adaptive"}}
      ]);
      self.optimalParams = ko.observable({})

      // self.init = function() {
      //   //make an api call to retrieve models and hyperparams
      //   var test =["1212", '1121',"74654"];
      //   var dummyModels = [{value: "KNN", model: "K Nearest Neighbors"}, {value: "DTREE", model: "Decision Trees"}, {model: "Neural Networks", value: "NN"}]
      // }

      // self.modelSelected = ko.observable("KNN");
      self.modelSelected = ko.observable();
      // self.selectedHyperParams = ko.observable();
      self.hyperParamsSelected = ko.observableArray();
      self.modelList = ko.observableArray();
      self.dummyParams = [] // to be replaced by api call
      // self.init();






      self.hyperParamSubmit = function() {
        console.log('initial hyper is ')
        console.log(self.hyperParamsSelected());
        var temp = {}
        temp.mode = self.modelSelected();
        var copiedObject = $.extend(true, {}, self.hyperParamsSelected())
        // temp.parameters = self.hyperParamsSelected();
        temp.parameters = copiedObject;
        for(var param in temp.parameters) {
          val = temp.parameters[param]
          console.log('val is');
          console.log(val)
          var paramRange = val.split(" ");
          temp.parameters[param] = paramRange;
        }
        console.log(temp)
        temp = JSON.stringify(temp);
        console.log('self hyperparam is')
        console.log(self.hyperParamsSelected())



        $.ajax
        ({
            type: "POST",
            //the url where you want to sent the userName and password to
            url: self.url,
            dataType: 'json',
            async: true,
            //json object to sent to the authentication url
            data: temp,
            contentType: 'application/json',
            success:  (response) => {
              console.log(JSON.parse(response))
              self.parseResponseParams(JSON.parse(response));
            }
        })
      }

    self.parseResponseParams = function(response) {
      self.optimalParams(response);
      console.log('self.optimalParams is ');
      console.log(self.optimalParams());
      self.displayOptimal = true;
    }




      //functions
      


      self.loadHyperparams = function() {
        console.log("the available params are:");
        self.dummyModels().forEach((elem, idx) => {
          if(elem.value === self.modelSelected()) {
            console.log(elem.hyperparams)
            // console.log(Object.keys(elem.hyperparams))
            self.hyperParamsSelected(elem.hyperparams)
            console.log(Object.keys(self.hyperParamsSelected()))
          }
        });
      }



      // Below are a set of the ViewModel methods invoked by the oj-module component.
      // Please reference the oj-module jsDoc for additional information.

      /**
       * Optional ViewModel method invoked after the View is inserted into the
       * document DOM.  The application can put logic that requires the DOM being
       * attached here. 
       * This method might be called multiple times - after the View is created 
       * and inserted into the DOM and after the View is reconnected 
       * after being disconnected.
       */
      self.connected = function() {
        // Implement if needed
      //   this.val = ko.observable("CH");
      // this.yoo = "afdfs"
      };

      /**
       * Optional ViewModel method invoked after the View is disconnected from the DOM.
       */
      self.disconnected = function() {
        // Implement if needed
      };

      /**
       * Optional ViewModel method invoked after transition to the new View is complete.
       * That includes any possible animation between the old and the new View.
       */
      self.transitionCompleted = function() {
        // Implement if needed
      };
    }
    /*
     * Returns a constructor for the ViewModel so that the ViewModel is constructed
     * each time the view is displayed.  Return an instance of the ViewModel if
     * only one instance of the ViewModel is needed.
     */
    return new DashboardViewModel();
  }
);
