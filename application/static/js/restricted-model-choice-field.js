(function(){
  function throwError(baseElement, message) {
    console.error(message, baseElement);
    throw new Error(message);
  }

  function reset(baseElement) {
    baseElement.value = "";
  }

  function getRestrictedFields() {
    return Array.prototype.slice.apply(document.querySelectorAll("[data-restrictions]"));
  }

  function getFieldsRestrictedOn(baseElement) {
    let elements = getRestrictedFields();
    return elements.filter(e => getRestrictedOnField(e) === baseElement);
  }

  function isFormsetTemplate(baseElement) {
    return baseElement.name.indexOf("__prefix__") >= 0;
  }

  function getRestrictedOnField(baseElement) {
    if (isFormsetTemplate(baseElement)) {
      return null;
    }

    let fieldName = baseElement.getAttribute("data-restricted-on");
    if (!fieldName) {
      throwError(baseElement, "data-restricted-on is undefined");
    }

    if (fieldName.indexOf("__prefix__") >= 0) {
      fieldName = cleanDynamicFormSetName(baseElement, fieldName);
    }

    let form = baseElement.closest("form");
    if (!form) {
      throwError(baseElement, "The field is not inside a form");
    }

    let fields = form.querySelectorAll(`[name=${fieldName}]`);
    if (fields.length == 0) {
      throwError(baseElement, `Could not find field ${fieldName}`);
    }

    if (fields.length > 1) {
      console.warn(`Found multiple fields ${fieldName}`);
    }
    return fields[0];
  }

  function cleanDynamicFormSetName(baseElement, fieldName) {
    let prefixIx = fieldName.indexOf("__prefix__");
    let selfPrefix = baseElement.name.slice(prefixIx);
    let prefixMatch = selfPrefix.match(/\d+/);
    if (!prefixMatch) {
      throwError(baseElement, `Cannot detect dynamic formset prefix: ${baseElement.name}`);
    }

    return fieldName.replace("__prefix__", prefixMatch[0]);
  }

  function getRestrictions(baseElement) {
    let restrictionsJson = baseElement.getAttribute("data-restrictions");
    if (!restrictionsJson) {
      throwError(baseElement, "data-restrictions is undefined");
    }

    return JSON.parse(restrictionsJson);
  }

  function updateOptionList(baseElement) {
    if (isFormsetTemplate(baseElement)) {
      return;
    }

    let refField = getRestrictedOnField(baseElement);
    if (!refField) {
      throwError(baseElement, "Could not find refField");
    }

    let restrictions = getRestrictions(baseElement);

    let options = Array.prototype.slice.apply(baseElement.querySelectorAll("option"));
    options.forEach(option => {
      if (!option.value) {
        option.hidden = false;
        return;
      }

      let allowedOnValues = restrictions[option.value] || [];
      option.hidden = allowedOnValues.indexOf(refField.value) < 0;
    });
  }

  function clearOptionList(baseElement) {
    let options = Array.prototype.slice.apply(baseElement.querySelectorAll("option"));
    options.forEach(option => {
      option.hidden = true;
    });
  }

  document.addEventListener("change", event => {
    let element = event.target;
    getFieldsRestrictedOn(element).forEach(baseElement => {
      reset(baseElement);
      updateOptionList(baseElement);
      baseElement.dispatchEvent(new Event("change", {bubbles: true}));
    });
  });

  document.addEventListener("DOMContentLoaded", () => {
    getRestrictedFields().forEach(baseElement => {
      if (isFormsetTemplate(baseElement)) {
        clearOptionList(baseElement);
      } else {
        updateOptionList(baseElement);
      }
    });
  })
})();