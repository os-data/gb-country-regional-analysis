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
      "fields": [
        {"column": "dept_code", "datatype": "string", "name": "name"},
        {"column": "dept_name", "datatype": "string", "name": "label"},
        {"constant": "true", "datatype": "constant", "name": "gov_department"}
      ],
      "label": "Paid from",
      "description": "The entity that the money was paid from"
    },
    "to": {
      "type": "entity",
      "fields": [
        {"constant": "society", "datatype": "constant", "name": "name"},
        {"constant": "Society (the General Public)", "datatype": "constant", "name": "label"},
        {"constant": "A dummy entity to be the recipient of final government spending.", "datatype": "constant", "name": "description"}
      ],
      "label": "Paid to",
      "description": "The entity that the money was paid to"
    },
    "time": {
      "type": "value",
      "column": "tax_year",
      "label": "Tax year",
      "description": "The accounting period in which the spending happened",
      "datatype": "date"
    },
    "amount": {
      "column": "amount",
      "label": "",
      "description": "",
      "datatype": "float",
      "type": "value"
    },
    "pog": {
      "type": "classifier",
      "fields": [
        {"column": "pog", "datatype": "string", "name": "name"},
        {"column": "pog_alias", "datatype": "string", "name": "label"}
      ],
      "label": "Programme Object Group",
      "taxonomy": "cra-pog"
    },
    "cap_or_cur": {
      "type": "classifier",
      "fields": [
        {"column": "cap_or_cur", "datatype": "string", "name": "label"}
      ],
      "label": "Capital/current",
      "description": "Capital (one-off investment) or Current (on-going running costs)",
      "taxonomy": "cra-cap_or_cur"
    },
    "cg_lg_or_pc": {
      "type": "classifier",
      "fields": [
        {"column": "cg_lg_or_pc", "datatype": "string", "name": "label"}
      ],
      "label": "CG, LG or PC",
      "description": "Central government, local government or public corporation",
      "taxonomy": "cra-cg_lg_or_pc"
    },
    "region": {
      "type": "classifier",
      "fields": [
        {"column": "nuts_region", "datatype": "string", "name": "label"}
      ],
      "label": "Geographic region",
      "description": "Geographical (NUTS) area for which money was spent",
      "taxonomy": "cra-region"
    },
    "hmt1": {
      "type": "classifier",
      "fields": [
        {"column": "hmt_functional", "datatype": "string", "name": "label"}
      ],
      "label": "HMT Function",
      "description": "HMT Functional Classification (Treasury equivalent of COFOG1)",
      "taxonomy": "cra-hmt-level1"
    },
    "hmt2": {
      "type": "classifier",
      "fields": [
        {"column": "hmt_subfunctional", "datatype": "string", "name": "label"}
      ],
      "label": "HMT Sub-function",
      "description": "HMT Sub-functional Classification (Treasury equivalent of COFOG2)",
      "taxonomy": "cra-hmt-level2"
    },
    "cofog1": {
      "type": "classifier",
      "fields": [
        {"column": "wdmmg_cofog1_color", "datatype": "string", "name": "color", "default_value": "#555555"},
        {"column": "cofog_level1_code", "datatype": "string", "name": "name", "default_value": "unknown"},
        {"column": "cofog_level1_name", "datatype": "string", "name": "label", "default_value": "Unknown"}
      ],
      "label": "COFOG level 1",
      "description": "Classification Of Function Of Government, level 1",
      "taxonomy": "cofog-1"
    },
    "cofog2": {
      "type": "classifier",
      "fields": [
        {"column": "wdmmg_cofog2_color", "datatype": "string", "name": "color", "default_value": "#555555"},
        {"column": "cofog_level2_code", "datatype": "string", "name": "name", "default_value": "unknown"},
        {"column": "cofog_level2_name", "datatype": "string", "name": "label", "default_value": "Unknown"}
      ],
      "label": "COFOG level 2",
      "description": "Classification Of Function Of Government, level 2",
      "taxonomy": "cofog-2"
    },
    "cofog3": {
      "type": "classifier",
      "fields": [
        {"column": "wdmmg_cofog3_color", "datatype": "string", "name": "color", "default_value": "#555555"},
        {"column": "cofog_level3_code", "datatype": "string", "name": "name", "default_value": "unknown"},
        {"column": "cofog_level3_name", "datatype": "string", "name": "label", "default_value": "Unknown"}
      ],
      "label": "COFOG level 3",
      "description": "Classification Of Function Of Government, level 3",
      "taxonomy": "cofog-3"
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
      "filters": {"taxonomy": "cofog-1"}
    },
    {
      "entity": "classifier",
      "label": "Spending by tertiary function",
      "name": "default",
      "dimension": "cofog2",
      "breakdown": "cofog3",
      "filters": {"taxonomy": "cofog-2"}
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
      "filters": {"taxonomy": "cofog-1"}
    },                              
    {
      "entity": "classifier",
      "label": "Spending by region (within secondary function)",
      "name": "region",
      "dimension": "cofog2",
      "breakdown": "region",
      "filters": {"taxonomy": "cofog-2"}
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
