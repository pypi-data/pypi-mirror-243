from lxml import etree
import copy
import re


class ElementBase(etree.ElementBase):
    """This class extends the etree.ElementBase class.
    It has many additional userfriendly methods
    """

    @property
    def ns(self):
        """Readonly property.

        :returns: namespace of the element
        """
        return etree.QName(self).namespace

    def qn(self, name, nsmap=None):
        """Handy method to get a qualified name from given arguments

        :param name: prefixed or un-prefixed element name.
        :param nsmap: dict with key as prefix and value as namespace
        :returns: fully qualified name (qn)


        if nsmap is None, self.nsmap is used.
        if name has no prefix and nsmap do not have None returns name.
        if name has no prefix then nsmap must have None map.

        Example::

            # when self.nsmap -> {}
            self.qn('some')                         #-> 'some'
            self.qn('some', {None:'http://bar'})    #-> '{http://bar}some'
            self.qn('c:some', {'c':'http://bar'})   #-> '{http://bar}some'
            self.qn('c:some')                       #-> KeyError: 'c'
            self.qn('c:some', {None:'http://bar'})  #-> KeyError: 'c'


            # when self.nsmap -> {None: 'http://foo/ns', 'd':'htpp://deck/ns'}
            self.qn('some')                         #-> '{http://foo/ns}some'
            self.qn('some', {None:'http://bar'})    #-> '{http://bar}some'
            self.qn('c:some', {'c':'http://bar'})   #-> '{http://bar}some'
            self.qn('c:some')                       #-> KeyError: 'c'
            self.qn('c:some', {None:'http://bar'})  #-> KeyError: 'c'
            self.qn('d:some')                       #-> '{htpp://deck/ns}some'
        """
        if nsmap is None:
            nsmap = self.nsmap

        if ':' in name:
            pfx, name = name.split(':')
        else:
            pfx = None

        if (pfx is None) and (None not in nsmap):
            return name

        return '{%s}%s' % (nsmap[pfx], name)

    @property
    def ln(self):
        """Handy readonly property to get a local name of this element

        :returns: local name

        Example::

            # self.tag == '{http://some/ns}elemTag' -> self.ln == 'elemTag'
            # self.tag == 'chart'                   -> self.ln == chart
        """
        return etree.QName(self).localname

    def me(self, *args, **kwargs):
        """Alias for makeelement method
        See the definition of makelement method of etree.Elementbase
        for more details
        """
        return self.makeelement(*args, **kwargs)

    def meqn(self, tag, attrib=None, nsmap=None):
        """meqn is an abbreviation for makeelementqualifiedname

        :param tag: It could be plane tag or tag with prefix eg. 'Relationship'
            or 'c:chart'
        :param attrib: It is dictionary with string key and string val. These
            will be attributes of the xml element
        :param nsmap: If nsmap is None then nsmap of this element is used to
            resolve the prefix of the given tag
        :returns: created element object

        Example::

            # When self.nsmap == {}
            self.meqn('c:chart')                            \
#-> Keyerror
            self.meqn('foo')                                \
#-> element obj with tag 'foo'
            self.meqn('a:foo', nsmap={'a':'http://Aaa/ns'}) \
#-> <{http://Aaa/ns}foo/>

            self.meqn('a:foo', attrib={'val':'1'}, nsmap={'a':'http://Aaa/ns'})
                # -> <{http://Aaa/ns}foo "val"="1"/>

            # when self.nsmap == {None: 'http://foo/ns', 'd':'htpp://deck/ns'}
            self.meqn('some')                               \
#-> '{http://foo/ns}some'
            self.meqn('some', nsmap={None:'http://bar'})    \
#-> '{http://bar}some'
            self.meqn('c:some', nsmap={'c':'http://bar'})   \
#-> '{http://bar}some'
            self.meqn('c:some')                             \
#-> KeyError: 'c'
            self.meqn('c:some', nsmap={None:'http://bar'})  \
#-> KeyError: 'c'
            self.meqn('d:some')                             \
#-> '{htpp://deck/ns}some'
        """
        if nsmap is None:
            nsmap = self.nsmap
        tag = self.qn(tag, nsmap)
        if isinstance(attrib, dict):
            attrib = {self.qn(i, nsmap): j for i, j in attrib.items()}
        return self.makeelement(tag, attrib, nsmap)

    def dump(self, *args, **kwargs):
        """Alias method for etree.dump
        See etree.dump for more information.
        """
        return etree.dump(self, *args, **kwargs)

    def deepcopy(self, *args, **kwargs):
        """Alias method for copy.deepcopy.
        See copy.deepcopy for more information

        :returns: duplicate of this element
        """
        return copy.deepcopy(self, *args, **kwargs)

    def getqn(self, key, default=None):
        """Similar to self.get with additional flexibility. It can resolve the
        key with prefixes

        :param key: element's attribute name
        :param default: this value would be returned when element do not have \
key attribute

        :returns: value or default of the key attribute of this element

        Example::

            # for element <c:somename val="0", r:id="rId3"/>
            e.getqn("val") = "0"
            e.getqn("r:id") = "rId3"
        """
        key = self.qn(key)
        return self.get(key, default)

    def setqn(self, key, value):
        """Similar to self.set with additional flexibility. It can resolve the
        key with prefixes

        :param key: element's attribute name
        :param value: key attribute of this element is set with the value

        Example::

            # for element <c:somename val="0", r:id="rId3"/>
            e.setqn("val") = "1"
            e.setqn("r:id") = "rId5"

            # element would be now <c:somename val="1", r:id="rId5"/>
        """
        self.set(self.qn(key), value)

    def findallqn(self, path, namespaces=None):
        """Similar to self.findall() with additional functionality of resolving
        path with prefixes

        :param path: prefixed name paths, normal paths
        :param namespaces: dictionary of prefix as key and namespace as value

        :return: list of elements matching the given parameters

        Examples::

            e.findallqn("c:chart//c:areaChart/c:axId")
            # [<Element {http://schemas.openxmlformats.org/drawingml/2006/\
chart}axId at 0x189d739f7a0>,
            #  <Element {http://schemas.openxmlformats.org/drawingml/2006/\
chart}axId at 0x189d739f7f0>]

            e.findallqn("./c:chart//c:areaChart/c:axId[@val="123456"]")
        """
        path = self._resolve_xpath(path, namespaces)
        return self.findall(path)

    def findqn(self, path, namespaces=None):
        """Similar to self.find() with additional funtionality of resolving
        path with prefixes.

        Example::

            # Following paths would be resolved to paths as shown below and \
passed to
            # self.find() method and its return value is returned
            'Relationship'      # -> 'Relationship'
            './Relationship'    # -> './Relationship'
            './/dummy'          # -> './/dummy'

            # when self.nsmap = {'c':'http://cee/ns', 'r':'http://ree/ns'}
            './/c:autoUpdate'   # -> './/{http://cee/ns}autoUpdate'
            './c:chart//'       # -> './{http://cee/ns}chart//'
            './/c16:uniqueId'   # -> './/{http://c16/ns}uniqueId' \
when namespaces = {'c16':'http://c16/ns'}


            './c:chart//c:axId[@val="505253232"]'
                # -> './{http://cee/ns}chart//{http://cee/ns}axId[@val=\
"505253232"]'
        """

        path = self._resolve_xpath(path, namespaces)
        return self.find(path)

    def rm(self):
        """Removes the current element from its parent.
        Limitation: it throws AttributeError when trying to remove root element
        """
        self.getparent().remove(self)

    def __getattr__(self, name, *args, **kwargs):
        """This special method is called when there is no attribute with name
        <name> in the element object. This method looks for a element as per
        the <name> as below.

        Limitation:
        Cannot be used to search element with attribute value. If element names
        have underscores in it, this method would not result proper results

        Exaxmples::

            # three underscores indicates './/'
            # two underscores indicates './'

            self.c_autoUpdate   #-> self.find('{http://cee/ns}autoUpdate')
            self.___c_chart     #-> self.find('.//{http://cee/ns}autoUpdate')
            self.__c_chart      #-> self.find('./{http://cee/ns}autoUpdate')

            self.c_chart___c_areaChart
                #-> self.find('{http://cee/ns}chart//{http://cee/ns}areaChart')
            c:externalData r:id="rId3
            self.c_externalData_r_id
                #-> self.find({http://cee/ns}externalData[@{http://ree/ns}id]')
            self.___mc_Choice   #-> though self.nsmap does not have namespace
                # for prefix 'mc' this method would scan all the child elements
                # of this element and tries to find an element matching given
                # path in terms of <name>
        """
        any_level = True if name.startswith('___') else False
        e = self
        for token_underscore3 in name.split('___'):
            if token_underscore3 == '':
                continue
            for token in token_underscore3.split('__'):
                if token == '':
                    continue
                if e is None:
                    return

                pre = ".//" if any_level else "./"
                tokens = token.split('_')
                if any(map(lambda t: t == '', tokens)):
                    return
                e_backup = e
                if len(tokens) == 1:
                    e = e.find(pre+token)

                elif len(tokens) == 2:
                    # ns, ln
                    pfx, ln = tokens
                    if pfx in e.nsmap:
                        ns = e.nsmap[pfx]
                        e = e.find(pre+'{'+ns+'}'+ln)
                    else:
                        # ln, attr
                        ln, attr = tokens
                        e = e.find(pre+ln+'[@'+attr+']')
                    if e is None and pfx not in e_backup.nsmap:
                        pfx, ln = tokens
                        lst_ns = self._get_lst_ns_from_children(e_backup, pfx)
                        for ns in lst_ns:
                            e = e_backup.find(pre+'{'+ns+'}'+ln)
                            if e is not None:
                                break

                elif len(tokens) == 3:
                    # ns ln attr
                    pfx, ln, attr = tokens
                    if pfx in e.nsmap:
                        ns = e.nsmap[pfx]
                        e = e.find(pre+'{'+ns+'}'+ln+'[@'+attr+']')
                    else:
                        # ln ns attr
                        ln, pfx, attr = tokens
                        if pfx in e.nsmap:
                            ns = e.nsmap[pfx]
                            e = e.find(pre+ln+'[@{'+ns+'}'+attr+']')

                    if e is None:
                        pfx, pfx2 = tokens[:2]
                        nsmap = e_backup.nsmap
                        if pfx not in nsmap and pfx2 not in nsmap:
                            # search for new ns
                            # pfx
                            lst_ns = self._get_lst_ns_from_children(
                                e_backup, pfx)
                            for ns in lst_ns:
                                e = e.find(pre+'{'+ns+'}'+ln+'[@'+attr+']')
                                if e is not None:
                                    break

                            # pfx2
                            if e is None:
                                lst_ns = self._get_lst_ns_from_children(
                                    e_backup, pfx2)
                                for ns in lst_ns:
                                    e = e.find(pre+ln+'[@{'+ns+'}'+attr+']')
                                    if e is not None:
                                        break
                elif len(tokens) == 4:
                    # ns, ln, ns, attr
                    pfx, ln, pfx2, attr = tokens
                    if pfx in e.nsmap:
                        lst_ns = [e.nsmap[pfx]]
                    else:
                        lst_ns = self._get_lst_ns_from_children(e, pfx)

                    if pfx2 in e.nsmap:
                        lst_ns2 = [e.nsmap[pfx2]]
                    else:
                        lst_ns2 = self._get_lst_ns_from_children(e, pfx2)

                    for ns in lst_ns:
                        for ns2 in lst_ns2:
                            e = e_backup.find(pre+'{'+ns+'}'+ln +
                                              '[@{'+ns2+'}'+attr+']')
                            if e is not None:
                                break
                        if e is not None:
                            break
                else:
                    return None

                any_level = False
            any_level = True
        return e

    def _get_lst_ns_from_children(self, parent, pfx):
        """Supporting method to get the list of namespaces for the given prefix
        It searches all the elements in the parent element
        """
        lst = []
        for e in parent.iter():
            if pfx in e.nsmap:
                lst.append(e.nsmap[pfx])
        return lst

    def _resolve_xpath(self, path, namespaces):
        """ Resolves the prefixes in the given path and return a fully
        qualified path

        Example::

            #Following paths would be resolved to paths as shown below and
            #passed to self.find() method and its return value is returned

            'Relationship'      #-> 'Relationship'
            './Relationship'    #-> './Relationship'
            './/dummy'          #-> './/dummy'

            # when self.nsmap = {'c':'http://cee/ns', 'r':'http://ree/ns'}
            './/c:autoUpdate'   #-> './/{http://cee/ns}autoUpdate'
            './c:chart//'       #-> './{http://cee/ns}chart//'
            './/c16:uniqueId'   #-> './/{http://c16/ns}uniqueId'
                #when namespaces={'c16':'http://c16/ns'}

            './c:chart//c:axId[@val="505253232"]'
            #-> './{http://cee/ns}chart//{http://cee/ns}axId[@val="505253232"]'
        """
        nsmap = self.nsmap
        if isinstance(namespaces, dict):
            nsmap.update(namespaces)
        lst_i = []
        for i in re.split('//', path):
            lst_j = []
            for j in re.split('/', i):
                tmp = j.split('[', maxsplit=1)
                name = tmp[0]
                remain = ''
                if len(tmp) == 2:
                    m = re.match(r'@([a-zA-Z:0-9]*)(.*)?', tmp[1])
                    if m:
                        attr = m[1]
                        remain = m[2]
                        try:
                            attr = self.qn(attr, nsmap=nsmap)
                        except KeyError:
                            pass
                        remain = '[@{}{}'.format(attr, remain)
                    else:
                        remain = '['+tmp[1]
                if name.isalnum() or re.match(r'\w+:\w+', name):
                    name = self.qn(name, nsmap=nsmap)
                lst_j.append(name+remain)
            path_j = '/'.join(lst_j)
            lst_i.append(path_j)
        path = '//'.join(lst_i)
        return path
