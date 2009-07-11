var shortcuts = new Hash({
  'p': 'python',
  'j': 'js',
  'h': 'html',
  's': 'sql',
  'b': 'bash',
  'c': 'css',
  'space': function(){
    $('lexer').focus();
    return false;
  },
  'enter': function(){
    $('pasteform').submit();
    return false;
  }
});

var boundValues = new Hash();
shortcuts.each(function(value, shortcut) {
  if ($type(value) == 'string') {
    boundValues.set(value, shortcut);
  }
});

window.addEvent('keydown', function(event){
  if (event.alt && !(event.meta || event.control)) {
    var s = shortcuts.get(event.shift ? event.key.toUpperCase() : event.key);
    switch ($type(s)) {
      case 'string':
        $('lexer').set('value', s);
        return false;
      case 'function':
        return s.call(event);
    }
  }
});

function updateShortcutTitles(lexerElem, submitElem) {
  lexerElem.getElements("option").each(function(optElem) {
    var shortcut = boundValues.get(optElem.get('value'));
    if (!shortcut) {
      return;
    }
    var shortcutHTML = ' &#8211; ';
    if (shortcut == shortcut.toUpperCase()) {
      shortcutHTML += '&#8679;'
    }
    shortcutHTML += '&#8997;' + shortcut.toUpperCase();
    optElem.set('html', optElem.get('html') + shortcutHTML);
  });
  var labelElem = lexerElem.getParent('label');
  labelElem.set('html', labelElem.get('html') + ' &#8211; &#8997; Space');
  submitElem.value=submitElem.get('value') + ' ⌥↩';
}

window.addEvent('domready', function(){
  updateShortcutTitles($("lexer"), $("make_pasta"));
  $('code').focus();
  $('lexer').addEvent('change', function() {
    if (this.get('value') != 'not_in_list') {
      return;
    }
    var textInput = new Element('input',
      {type: 'text', value: 'text', name: 'lexer'});
    textInput.inject('lexer', 'after');
    textInput.focus();
    this.destroy();
  });
});
