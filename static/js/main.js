/**
 * O HI. I AM AN ORANGUTANG, WOOPA WOOPA
 *
 * Copyright (c) Send a Patch <ludvig@sendapatch.se>, 2010
 */

/**
 * Why does JavaScript not have this?
 */
String.prototype.endsWith = function(v) {
  return this.substring(this.length - v.length) == v;
};

/**
 * Keyboard shortcuts
 */
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
    $$(".bambutton").getParent("form")[0].submit();
    return false;
  }
});

/**
 * Reverse mapping of lexer names to keyboard shortcuts (skips non-lexer
 * shortcuts)
 */
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

function updateShortcutTitles(force) {
  var lexerEl = $("lexer");

  lexerEl.getElements("option").each(function(optEl) {
    var shortcut = boundValues.get(optEl.get('value'));
    if (!shortcut)
      return;

    var shortcutHTML = ' &#8211; ';
    if (shortcut == shortcut.toUpperCase()) {
      shortcutHTML += '&#8679;'
    }
    shortcutHTML += '&#8997;' + shortcut.toUpperCase();

    optEl.set('html', optEl.get('html') + shortcutHTML);
  });

  var labelEl = lexerEl.getParent('label');
  labelEl.set('html', labelEl.get('html') + ' &#8211; &#8997; Space');

  var bamEl = $$(".bambutton")[0];
  if (bamEl && !bamEl.value.endsWith(' ⌥↩'))
    bamEl.value += ' ⌥↩';
}

/**
 * Convert the dropdown to a text input if "manual selection" is clicked.
 */
function rebuildLexerIntoText() {
  if (this.get('value') != 'not_in_list')
    return;

  var textInput = new Element(
      'input',
      {type: 'text', value: 'text',
       name: this.name, id: this.id});
  textInput.inject(this.id, 'after');
  textInput.focus();
  this.destroy();
}


                                               /*'    ,c
                                                 "?c   JF
                                                   `?  $
                                             =="""==   "
                                                 ,ccu,d??b,
                                              ,r"",,"",cc,"u
                                              F z$$$  $??$,?b.
                                           zcu" P"  .%   ` ,zc,
                                          JP""$i  ,u"u^=="zP"??b
                .,,,,.                    4L d$$$ccc$$$$$$$$$u-$
           ,cc$$$$$$$$b                   `$ $$$$$$$$$$$$$$$$bc
       uc$$$$$P$$?$$$$$c                   "J$$$$$$$$$$$$$$$$$$.
   _ud$$$$$$$PF:?:$$$$$$,                   $$$$$$$$$$$$$$$$$$$b
  `"""""         4$$$$$$$                  <$$$$$$$$$$$$$P??$$$$
                 $$$$$$$$.                 `$$$$$P??$$$$$L,J$$$%
                J$$$$$$$$b                  ?$$$$L,J$$$$$$$$$$"
                $$$$$$$$$$.                  "?$$$$$$$$$$$$P"
               J$$$$$$$$$$b                     ""?????""
               $$$$$$$$$$$$                       ?b,,,,c$F
              d$$$$$$$$$$$$,                       $$$$$$$
             4$$$$$$$$$$$$$$                       ^$$$$$$F
             $$$$$$$$$$$$$$$                        $$$$$$L
            4$$$$$$$$$$$$$$$,                       $$$$$$$
            $$$$$$$$$$$$$$$$$                    ;' `????"".,!
           4$$$$$$$$$$$$$$$$$                    `!!!!!!!!!!!!
           $$$$$$$$$$$$$$$$$$,                    !!!!!!!!!''
          4$$$$$$$$$$$$$$$$$$h                     ,,     =cc
          d$$$$$$$$$$$$$$$$$$$                  ,udF        $,
          $$$$$$$$$$$$$$$$$$$$.              , ' ?$b.      ,$b
         J$$$$$$$$$$$$bu,"???$F        _,,u'     z$$$cc,,zd$$$b
         $$$$$$$$$$$$$$P"  ~  ~  -  ~   ?$$$cccd$$$$$$$$$$$$$$$,
         $$$$$$$$$$$$F                   $$$$$$$$$$$$$$$$$$$$$$$.
        J$$$$$$$$$$$$r                ,z$???$$$$$$$$$$$$$$$$$$$$$
        $$$$$$PF"""$$$c,.        .,ccP"     <$$$$$$$$$$$$$$$$$$$$i
        $$$$$F     ,$$$$$$$$$$$$$$$$$     ,c$$$$$$$$$$$$$$$$$$$$$$.
        $$$$$$c,zc$$$PF""  `"$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$b
        $$$$$$$$$$P"         `$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$
        $$$$$$$$P           ,c$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$;
        `$$$$$$$$u,      ,cd$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$F
         $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$;z,
          R$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ $$$,
            $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$P $$$$b
           J$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$ d$$$$?l.
          4$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$P c`??"zF;)
          $$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$P"u$$$$$bccP"
         $$$$$C"?$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$P".`??$PF""
        ,$$$$$$$c ??$$$$$$$$$$$$$$$F?$$$$$$$$$C"$$$$$$$$$P"   3 c \
        $$$$$$$$$$bc.`??$$$$$$$$$$$$ 3$$$$$$$??b ?$$$$P"      4 `b "
        $$$$$$$$$$P")zbcc `""????$$$b ?$$$"xcc= b.""             "
        \ = 4$$$$$$$$PF",c             ?$$$e.",,$$
         `?)J$PFFF"" u 3 $              ?$$$$$$$$$$
                   ,F J' $               `$$$$$$$$$L
                     4'  "                 ?$$$$$$$$.
                                            `?$$$$$$b
                                               ""????_,,__
                                                    $`?c,"""
                                                    ?F `?c
                                                     */
