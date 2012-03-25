{
  "dataset": {
    "model_rev": 1,
    "name": "ukgov-finances-cra",
    "label": "UK Country Regional Analysis",
    "description": "The Country Regional Analysis published by HM Treasury (2010 version).\n\nSource data can be found in the [CKAN data package](http://ckan.net/package/ukgov-finances-cra)",
    "currency": "GBP"
  },
  "mapping": {
    "from": {
      "type": "entity",
      "attributes": {
        "name": {
          "column": "dept_code",
          "datatype": "id"
        },
        "label": {
          "column": "dept_name",
          "datatype": "string"
        }
      },
      "label": "Paid from",
      "description": "The entity that the money was paid from",
      "facet": true
    },
    "time": {
      "type": "date",
      "datatype": "date",
      "column": "tax_year",
      "label": "Tax year",
      "description": "The accounting period in which the spending happened"
    },
    "amount": {
      "column": "amount",
      "label": "Amount",
      "description": "",
      "type": "measure",
      "datatype": "float",
      "default_value": "0.0"
    },
    "unique_id": {
      "column": "unique_id",
      "label": "Unique ID",
      "description": "Dataset-specific unique identifier for transaction",
      "datatype": "string",
      "type": "value",
      "datatype": "id",
      "key": true
    },
    "pog": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "pog",
          "datatype": "id"
        },
        "label": { 
          "column": "pog_alias",
          "datatype": "string"
        }
      },
      "label": "Programme Object Group",
      "facet": true
    },
    "cap_or_cur": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "cap_or_cur",
          "datatype": "id"
        },
        "label": { 
          "column": "cap_or_cur",
          "datatype": "string"
        }
      },
      "label": "Capital/current",
      "description": "Capital (one-off investment) or Current (on-going running costs)",
      "taxonomy": "cra-cap_or_cur",
      "facet": true
    },
    "cg_lg_or_pc": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "cg_lg_or_pc",
          "datatype": "id"
        },
        "label": { 
          "column": "cg_lg_or_pc",
          "datatype": "string"
        }
      },
      "label": "CG, LG or PC",
      "description": "Central government, local government or public corporation",
      "facet": true
    },
    "region": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "nuts_region",
          "datatype": "id"
        },
        "label": { 
          "column": "nuts_region",
          "datatype": "string"
        }
      },
      "label": "Geographic region",
      "description": "Geographical (NUTS) area for which money was spent",
      "facet": true
    },
    "hmt1": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "hmt_functional",
          "datatype": "id"
        },
        "label": { 
          "column": "hmt_functional",
          "datatype": "string"
        }
      },
      "label": "HMT Function",
      "description": "HMT Functional Classification (Treasury equivalent of COFOG1)",
      "facet": true
    },
    "hmt2": {
      "type": "classifier",
      "attributes": {
        "name": { 
          "column": "hmt_subfunctional",
          "datatype": "id"
        },
        "label": { 
          "column": "hmt_subfunctional",
          "datatype": "string"
        }
      },
      "label": "HMT Sub-function",
      "description": "HMT Sub-functional Classification (Treasury equivalent of COFOG2)",
      "facet": true
    },
    "cofog1": {
      "type": "classifier",
      "attributes": {
        "color": {
          "column": "wdmmg_cofog1_color",
          "default_value": "#555555",
          "datatype": "string"
        },
        "name": {
          "column": "cofog_level1_code",
          "default_value": "unknown",
          "datatype": "id"
        },
        "label": {
          "column": "cofog_level1_name",
          "default_value": "Unknown",
          "datatype": "string"
        }
      },
      "label": "COFOG level 1",
      "description": "Classification Of Function Of Government, level 1",
      "facet": true
    },
    "cofog2": {
      "type": "classifier",
      "attributes": {
        "color": {
          "column": "wdmmg_cofog2_color",
          "default_value": "#555555",
          "datatype": "string"
        },
        "name": {
          "column": "cofog_level2_code",
          "default_value": "unknown",
          "datatype": "id"
        },
        "label": {
          "column": "cofog_level2_name",
          "default_value": "Unknown",
          "datatype": "string"
        }
      },
      "label": "COFOG level 2",
      "description": "Classification Of Function Of Government, level 2",
      "facet": true
    },
    "cofog3": {
      "type": "classifier",
      "attributes": {
        "color": {
          "column": "wdmmg_cofog3_color",
          "default_value": "#555555",
          "datatype": "string"
        },
        "name": {
          "column": "cofog_level3_code",
          "default_value": "unknown",
          "datatype": "id"
        },
        "label": {
          "column": "cofog_level3_name",
          "default_value": "Unknown",
          "datatype": "string"
        }
      },
      "label": "COFOG level 3",
      "description": "Classification Of Function Of Government, level 3",
      "facet": true
    }
  },
  "views": [
    {
      "entity": "dataset",
      "label": "Spending by primary function",
      "name": "default",
      "dimension": "dataset",
      "breakdown": "cofog1",
      "filters": {"name": "ukgov-finances-cra"}
    },
    {
      "entity": "classifier",
      "label": "Spending by secondary function",
      "name": "default",
      "dimension": "cofog1",
      "breakdown": "cofog2",
      "filters": {"taxonomy": "cofog1"}
    },
    {
      "entity": "classifier",
      "label": "Spending by tertiary function",
      "name": "default",
      "dimension": "cofog2",
      "breakdown": "cofog3",
      "filters": {"taxonomy": "cofog2"}
    },
    {
      "entity": "dataset",
      "label": "Spending by government department",
      "name": "department",
      "dimension": "dataset",
      "breakdown": "from",
      "filters": {"name": "ukgov-finances-cra"}
    },
    {
      "entity": "dataset",
      "label": "Spending by region",
      "name": "region",
      "dimension": "dataset",
      "breakdown": "region",
      "filters": {"name": "ukgov-finances-cra"}
    },
    {
      "entity": "classifier",
      "label": "Spending by region (within primary function)",
      "name": "region",
      "dimension": "cofog1",
      "breakdown": "region",
      "filters": {"taxonomy": "cofog1"}
    },                              
    {
      "entity": "classifier",
      "label": "Spending by region (within secondary function)",
      "name": "region",
      "dimension": "cofog2",
      "breakdown": "region",
      "filters": {"taxonomy": "cofog2"}
    },
    {
      "entity": "entity",
      "label": "Spending by region (within department)",
      "name": "default",
      "dimension": "from",
      "breakdown": "region",
      "filters": {"gov_department": "true"}
    }
  ]
}
