/**
 * Created by ar on 11.09.16.
 */

'use strict';

angular.module('datasetImage2dPreview2', ['ngMaterial', 'datasetImage2dPaging', 'cl.paging'])
.component('datasetImage2dPreview2', {
    templateUrl: '/frontend/components/preview/dataset-image2d-preview/dataset-image2d-preview2.html',
    bindings: {
        databaseId:     '@',
        datasetType:    '@',
        listClasses:    '<'
    },
    controller: function ($scope, $http, dbinfoService) {
        var self = this;
        self.listClasses = [];
        self.$onInit = function () {
            self.listClasses = [];
            dbinfoService.getDatasetInfo('123').then(
                function successCallback(response) {
                    var tdata = response.data;
                    var lstKeys = Object.keys(tdata);
                    var tret=[];
                    for(var ii=0; ii<lstKeys.length; ii++) {
                        var tkey = lstKeys[ii];
                        var tnum = tdata[tkey];
                        tret.push({
                            info:   tkey,
                            idx:    tkey,
                            num:    tnum
                        });
                    }
                    self.listClasses = tret;
                    console.log(self.listClasses);
                }, function errorCallback(response) {
                    console.log(response);
                }
            );
        };
    }
});