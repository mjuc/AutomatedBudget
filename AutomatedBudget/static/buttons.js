var expTotal = 1;
var condTotal = 1;

function updateElementIndex(el, prefix, ndx) {
    var id_regex = new RegExp('(' + prefix + '-\\d+)');
    var replacement = prefix + '-' + ndx;
    el.id = el.id.replace(id_regex, replacement);
}

function copyElement(target) {
    var appendTarget = document.getElementById(target + "Form");
    src = document.getElementById(target);
    copy = src.cloneNode(true);
    if (target === 'exp')
    {
        updateElementIndex(copy,target,expTotal);
        expTotal++;
    }
    else if (target === 'cond')
    {
        updateElementIndex(copy,target,condTotal);
        condTotal++;
    }
    appendTarget.appendChild(copy);
    if (target === 'exp')
    {
        var previousRows = $('.exp-row:not(:last)');
        previousRows.find('.btn.add-exp-row')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-exp-row').addClass('remove-exp-row');
    }
    else if (target === 'cond')
    {
        var previousRows = $('.cond-row:not(:last)');
        previousRows.find('.btn.add-cond-row')
        .removeClass('btn-success').addClass('btn-danger')
        .removeClass('add-cond-row').addClass('remove-cond-row');
    }
    
}

function deleteElement(target, btn) {
    console.log("dupa")
    var total = ((target === 'exp') ? expTotal : condTotal);
    if (total > 1)
    {
        var forms;
        if (target === 'exp')
        {
            btn.closest('.exp-row').remove();
            total--;
            expTotal--;
            forms = $('.exp-row'); 
        }
        else if (target === 'cond')
        {
            btn.closest('.cond-row').remove();
            total--;
            condTotal--;
            forms = $('.cond-row');
        }
        for (var i=1, formCount = forms.length; i<formCount; i++)
        {
            updateElementIndex(forms[i],target,i)
        }
    }
}

$(document).on('click', '.add-exp-row' ,function(e){
    e.preventDefault();
    copyElement('exp');
})

$(document).on('click', '.add-cond-row' ,function(e){
    e.preventDefault();
    copyElement('cond');
})