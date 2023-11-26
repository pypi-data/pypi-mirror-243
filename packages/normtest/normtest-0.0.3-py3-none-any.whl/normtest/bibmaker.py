### DOCUMENTATTION ###
def docstring_parameter(*args, **kwargs):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*args, **kwargs)
        return obj

    return dec


BIB = {
    "type": "bib : file",
    "description": "The `citekey.bib` file (only if `export=True`)",
}
CITATION = {
    "type": "citation : str",
    "description": "The citation generated",
}
CITEKEY = {
    "type": "citekey : str",
    "description": "The name that is used to uniquely identify the entry;",
}

DATE = {
    "type": "date : str, optional",
    "description": "The publication date. If `date=None`, the `year` parameter must not be `None`;",
}


EXPORT = {
    "type": "export : bool, optional",
    "description": "Whether to export the `citekey.bib` file (`True`, default) or not (`False`);",
}


OPTIONALS = {
    "type": "**optionals : str",
    "description": "Optional fields for an techreport entry (`volume`, `number`, `pages`, etc).",
}

YEAR = {
    "type": "year : int, optional",
    "description": "The year of publication; If `year=None`, the `date` parameter must not be `None`;",
}


# PARAM = {
#     "type":
#     "description":
# }


### GENERAL ###
def empty_spaces(fields, field):
    return len(max(fields, key=len)) - len(str(field))


GENERIC_FIELDS_DESCRIPTION = {
    "abstract": (
        "field (literal)",
        "This field is intended for recording abstracts in a bib file, to be printed by a special bibliography style. It is not used by all standard bibliography styles.",
    ),
    "addendum": (
        "field (literal)",
        "Miscellaneous bibliographic data to be printed at the end of the entry. This is similar to the note field except that it is printed at the end of the bibliography entry.",
    ),
    "afterword": ("list (name)", "The author(s) of an afterword to the work."),
    "annotation": (
        "field (literal)",
        "This field may be useful when implementing a style for annotated bibliographies. It is not used by all standard bibliography styles. Note that this field is completely unrelated to annotator. The annotator is the author of annotations which are part of the work cited.",
    ),
    "annotator": (
        "list (name)",
        "The author(s) of annotations to the work. If the annotator is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also commentator.",
    ),
    "author": ("list (name)", "The author(s) of the title."),
    "authortype": (
        "field (key)",
        "The type of author. This field will affect the string (if any) used to introduce the author.",
    ),
    "bookauthor": ("list (name)", "The author(s) of the booktitle."),
    "bookpagination": (
        "field (key)",
        "If the work is published as part of another one, this is the pagination scheme of the enclosing work, i. e., bookpagination relates to pagination like booktitle to title.The key should be given in the singular form. Possible keys are page, column, line, verse, section, and paragraph.",
    ),
    "booksubtitle": (
        "field (literal)",
        "The subtitle related to the booktitle. If the subtitle field refers to a work which is part of a larger publication, a possible subtitle of the main work is given in this field. See also subtitle.",
    ),
    "booktitle": (
        "field (literal)",
        "If the title field indicates the title of a work which is part of a larger publication, the title of the main work is given in this field.",
    ),
    "booktitleaddon": (
        "field (literal)",
        "An annex to the booktitle, to be printed in a different font.",
    ),
    "chapter": ("field (literal)", "A chapter or section or any other unit of a work."),
    "commentator": (
        "list (name)",
        "The author(s) of a commentary to the work. Note that this field is intended for commented editions which have a commentator in addition to the author. If the work is a stand-alone commentary, the commentator should be given in the author field. If the commentator is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography.",
    ),
    "date": ("field (date)", "The publication date."),
    "doi": ("field (verbatim)", "The Digital Object Identifier of the work."),
    "edition": (
        "field (integer or literal)",
        "The edition of a printed publication. This must be an integer, not an ordinal. Don't say edition={First} or edition={1st} but edition={1}. The bibliography style converts this to a language dependent ordinal. It is also possible to give the edition as a literal string, for example “Third, revised and expanded edition”.",
    ),
    "editor": (
        "list (name)",
        "The editor(s) of the title, booktitle, or maintitle, depending on the entry type. Use the editortype field to specify the role if it is different from 'editor'.",
    ),
    "editora": (
        "list (name)",
        "A secondary editor performing a different editorial role, such as compiling, redacting, etc.",
    ),
    "editorb": (
        "list (name)",
        "Another secondary editor performing a different role. Use the editorbtype field to specify the role.",
    ),
    "editorc": (
        "list (name)",
        "Another secondary editor performing a different role. Use the editorctype field to specify the role.",
    ),
    "editortype": (
        "field (key)",
        "The type of editorial role performed by the editor. Roles supported by default are editor, compiler, founder, continuator, redactor, reviser, collaborator, organizer. The role 'editor' is the default. In this case, the field is omissible.",
    ),
    "editoratype": (
        "field (key)",
        "Similar to editortype but referring to the editora field.",
    ),
    "editorbtype": (
        "field (key)",
        "Similar to editortype but referring to the editorb field.",
    ),
    "editorctype": (
        "field (key)",
        "Similar to editortype but referring to the editorc field.",
    ),
    "eid": (
        "field (literal)",
        "The electronic identifier of an @article or chapter-like section of a larger work often called 'article number', 'paper number' or the like. This field may replace the pages field for journals deviating from the classic pagination scheme of printed journals by only enumerating articles or papers and not pages. Not to be confused with number, which for @articles subdivides the volume.",
    ),
    "entrysubtype": (
        "field (literal)",
        "This field, which is not used by the standard styles, may be used to specify a subtype of an entry type. This may be useful for bibliography styles which support a finergrained set of entry types.",
    ),
    "eprint": (
        "field (verbatim)",
        "The electronic identifier of an online publication. This is roughly comparable to a doi but specific to a certain archive, repository, service, or system.",
    ),
    "eprintclass": (
        "field (literal)",
        "Additional information related to the resource indicated by the eprinttype field. This could be a section of an archive, a path indicating a service, a classification of some sort, etc.",
    ),
    "eprinttype": (
        "field (literal)",
        "The type of eprint identifier, e. g., the name of the archive, repository, service, or system the eprint field refers to.",
    ),
    "eventdate": (
        "field (date)",
        "The date of a conference, a symposium, or some other event in @proceedings and @inproceedings entries. This field may also be useful for the custom types",
    ),
    "eventtitle": (
        "field (literal)",
        "The title of a conference, a symposium, or some other event in @proceedings and @inproceedings entries. This field may also be useful for the custom types. Note that this field holds the plain title of the event. Things like “Proceedings of the Fifth XYZ Conference” go into the titleaddon or booktitleaddon field, respectively.",
    ),
    "eventtitleaddon": (
        "field (literal)",
        "An annex to the eventtitle field. Can be used for known event acronyms, for example.",
    ),
    "file": (
        "field (verbatim)",
        "A local link to a pdf or other version of the work. Not used by the standard bibliography styles.",
    ),
    "foreword": (
        "list (name)",
        "The author(s) of a foreword to the work. If the author of the foreword is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also introduction and afterword.",
    ),
    "holder": (
        "list (name)",
        "The holder(s) of a @patent, if different from the author. Note that corporate holders need to be wrapped in an additional set of braces. This list may also be useful for the custom types listed.",
    ),
    "howpublished": (
        "field (literal)",
        "A publication notice for unusual publications which do not fit into any of the common categories.",
    ),
    "indextitle": (
        "field (literal)",
        "A title to use for indexing instead of the regular title field. This field may be useful if you have an entry with a title like “An Introduction to …” and want that indexed as “Introduction to …, An”. Style authors should note that biblatex automatically copies the value of the title field to indextitle if the latter field is undefined.",
    ),
    "institution": (
        "list (literal)",
        "The name of a university or some other institution, depending on the entry type. Traditional BibTeX uses the field name school for theses, which is supported as analias.",
    ),
    "introduction": (
        "list (name)",
        "The author(s) of an introduction to the work. If the author of the introduction is identical to the editor and/or translator, the standard styles will automatically concatenate these fields in the bibliography. See also foreword and afterword.",
    ),
    "isan": (
        "field (literal)",
        "The International Standard Audiovisual Number of an audiovisual work. Not used by the standard bibliography styles.",
    ),
    "isbn": ("field (literal)", "The International Standard Book Number of a book."),
    "ismn": (
        "field (literal)",
        "The International Standard Music Number for printed music such as musical scores. Not used by the standard bibliography styles.",
    ),
    "isrn": (
        "field (literal)",
        "The International Standard Technical Report Number of a technical report.",
    ),
    "issn": (
        "field (literal)",
        "The International Standard Serial Number of a periodical.",
    ),
    "issue": (
        "field (literal)",
        "The issue of a journal. This field is intended for journals whose individual issues are identified by a designation such as 'Spring' or 'Summer' rather than the month or a number. The placement of issue is similar to month and number. Integer ranges and short designators are better written to the number field.",
    ),
    "issuesubtitle": (
        "field (literal)",
        "The subtitle of a specific issue of a journal or other periodical.",
    ),
    "issuetitle": (
        "field (literal)",
        "The title of a specific issue of a journal or other periodical.",
    ),
    "issuetitleaddon": (
        "field (literal)",
        "An annex to the issuetitle, to be printed in a different font",
    ),
    "swc": (
        "field (literal)",
        "The International Standard Work Code of a musical work. Not used by the standard bibliography styles.",
    ),
    "journalsubtitle": (
        "field (literal)",
        "The subtitle of a journal, a newspaper, or some other periodical.",
    ),
    "journaltitle": (
        "field (literal)",
        "The name of a journal, a newspaper, or some other periodical.",
    ),
    "journaltitleaddon": (
        "field (literal)",
        "An annex to the journaltitle, to be printed in a different font.",
    ),
    "label": (
        "field (literal)",
        "A designation to be used by the citation style as a substitute for the regular label if any data required to generate the regular label is missing. For example, when an author-year citation style is generating a citation for an entry which is missing the author or the year, it may fall back to label. Note that, in contrast to shorthand, label is only used as a fallback. See also shorthand.",
    ),
    "language": (
        "list (key)",
        "The language(s) of the work. Languages may be specified literally or as localisation keys. If localisation keys are used, the prefix lang is omissible.",
    ),
    "library": (
        "field (literal)",
        "This field may be useful to record information such as a library name and a call number. This may be printed by a special bibliography style if desired. Not used by the standard bibliography styles.",
    ),
    "location": (
        "list (literal)",
        "The place(s) of publication, i. e., the location of the publisher or institution, depending on the entry type. Traditional BibTeX uses the field name address, which is supported as an alias. See also §§ 2.2.5 and 2.3.4. With @patent entries, this list indicates the scope of a patent. This list may also be useful for the custom types.",
    ),
    "mainsubtitle": (
        "field (literal)",
        "The subtitle related to the maintitle. See also subtitle.",
    ),
    "maintitle": (
        "field (literal)",
        "The main title of a multi-volume book, such as Collected Works. If the title or booktitle field indicates the title of a single volume which is part of multi-volume book, the title of the complete work is given in this field.",
    ),
    "maintitleaddon": (
        "field (literal)",
        "An annex to the maintitle, to be printed in a different font",
    ),
    "month": (
        "field (literal)",
        "The publication month. This must be an integer, not an ordinal or a string. Don't say month={January} but month={1}. The bibliography style converts this to a language dependent string or ordinal where required. This field is a literal field only when given explicitly in the data (for plain BibTeX compatibility for example). It is however better to use the date field as this supports many more features.",
    ),
    "nameaddon": (
        "field (literal)",
        "An addon to be printed immediately after the author name in the bibliography. Not used by the standard bibliography styles.",
    ),
    "note": (
        "field (literal)",
        "Miscellaneous bibliographic data which does not fit into any other field. The note field may be used to record bibliographic data in a free format. Publication facts such as 'Reprint of the edition London 1831' are typical candidates for the note field.",
    ),
    "number": (
        "field (literal)",
        "The number of a journal or the volume/number of a book in a series. See also issue. With @patent entries, this is the number or record token of a patent or patent request. Normally this field will be an integer or an integer range, but it may also be a short designator that is not entirely numeric such as 'S1', 'Suppl. 2', '3es'. In these cases the output should be scrutinised carefully. Since number is—maybe counterintuitively given its name—a literal field, sorting templates will not treat its contents as integers, but as literal strings, which means that '11' may sort between '1' and '2'. If integer sorting is desired, the field can be declared an integer field in a custom data model. But then the sorting of non-integer values is not well defined. The 'article number' or 'paper number', which can be used instead of—or along with—a page range to pinpoint a specific article within another work, goes into the eid field.",
    ),
    "organization": (
        "list (literal)",
        "The organization(s) that published a @manual or an @online resource, or sponsored a conference.",
    ),
    "origdate": (
        "field (date)",
        "If the work is a translation, a reprint, or something similar, the publication date of the original edition. Not used by the standard bibliography styles. See also date.",
    ),
    "origlanguage": (
        "list (key)",
        "If the work is a translation, the language(s) of the original work. See also language.",
    ),
    "origlocation": (
        "list (literal)",
        "If the work is a translation, a reprint, or something similar, the location of the original edition. Not used by the standard bibliography styles. See also location.",
    ),
    "origpublisher": (
        "list (literal)",
        "If the work is a translation, a reprint, or something similar, the publisher of the original edition. Not used by the standard bibliography styles. See also publisher",
    ),
    "origtitle": (
        "field (literal)",
        "If the work is a translation, the title of the original work. Not used by the standard bibliography styles. See also title.",
    ),
    "pages": (
        "field (range)",
        "One or more page numbers or page ranges. If the work is published as part of another one, such as an article in a journal or a collection, this field holds the relevant page range in that other work. It may also be used to limit the reference to a specific part of a work (a chapter in a book, for example). For papers in electronic journals with a non-classical pagination setup the eid field may be more suitable.",
    ),
    "pagetotal": ("field (literal)", "The total number of pages of the work."),
    "pagination": (
        "field (key)",
        "The pagination of the work. The value of this field will affect the formatting the hpostnotei argument to a citation command. The key should be given in the singular form. Possible keys are page, column, line, verse, section, and paragraph. See also bookpagination.",
    ),
    "part": (
        "field (literal)",
        "The number of a partial volume. This field applies to books only, not to journals. It may be used when a logical volume consists of two or more physical ones. In this case the number of the logical volume goes in the volume field and the number of the part of that volume in the part field. See also volume.",
    ),
    "publisher": ("list (literal)", "The name(s) of the publisher(s)."),
    "pubstate": (
        "field (key)",
        "The publication state of the work, e. g., 'in press'.",
    ),
    "reprinttitle": (
        "field (literal)",
        "The title of a reprint of the work. Not used by the standard styles.",
    ),
    "series": (
        "field (literal)",
        "The name of a publication series, such as “Studies in …”, or the number of a journal series. Books in a publication series are usually numbered. The number or volume of a book in a series is given in the number field. Note that the @article entry type makes use of the series field as well, but handles it in a special way.",
    ),
    "shortauthor": (
        "list (name)",
        "The author(s) of the work, given in an abbreviated form. This field is mainly intended for abbreviated forms of corporate authors.",
    ),
    "shorteditor": (
        "list (name)",
        "The editor(s) of the work, given in an abbreviated form. This field is mainly intended for abbreviated forms of corporate editors.",
    ),
    "shorthand": (
        "field (literal)",
        "A special designation to be used by the citation style instead of the usual label. If defined, it overrides the default label. See also label.",
    ),
    "shorthandintro": (
        "field (literal)",
        "The verbose citation styles which comes with this package use a phrase like “henceforth cited as [shorthand]” to introduce shorthands on the first citation. If the shorthandintro field is defined, it overrides the standard phrase. Note that the alternative phrase must include the shorthand.",
    ),
    "shortjournal": (
        "field (literal)",
        "A short version or an acronym of the journaltitle. Not used by the standard bibliography styles.",
    ),
    "shortseries": (
        "field (literal)",
        "A short version or an acronym of the series field. Not used by the standard bibliography styles.",
    ),
    "shorttitle": (
        "field (literal)",
        "The title in an abridged form. This field is usually not included in the bibliography. It is intended for citations in author-title format. If present, the author-title citation styles use this field instead of title.",
    ),
    "subtitle": ("field (literal)", "The subtitle of the work."),
    "title": ("field (literal)", "The title of the work."),
    "titleaddon": (
        "field (literal)",
        "An annex to the title, to be printed in a different font.",
    ),
    "translator": (
        "list (name)",
        "The translator(s) of the title or booktitle, depending on the entry type. If the translator is identical to the editor, the standard styles will automatically concatenate these fields in the bibliography.",
    ),
    "type": (
        "field (key)",
        "The type of a manual, patent, report, or thesis. This field may also be useful for the custom types",
    ),
    "url": (
        "field (uri)",
        "The url of an online publication. If it is not URL-escaped (no '%' chars) it will be URI-escaped according to RFC 3987, that is, even Unicode chars will be correctly escaped.",
    ),
    "urldate": (
        "field (date)",
        "The access date of the address specified in the url field.",
    ),
    "venue": (
        "field (literal)",
        "The location of a conference, a symposium, or some other event in @proceedings and @inproceedings entries. This field may also be useful for the custom types. Note that the location list holds the place of publication. It therefore corresponds to the publisher and institution lists. The location of the event is given in the venue field. See also eventdate and eventtitle.",
    ),
    "version": (
        "field (literal)",
        "The revision number of a piece of software, a manual, etc.",
    ),
    "volume": (
        "field (integer)",
        "The volume of a multi-volume book or a periodical. It is expected to be an integer, not necessarily in arabic numerals since biber will automatically convert from roman numerals or arabic letter to integers internally for sorting purposes. See also part. See the noroman option which can be used to suppress roman numeral parsing. This can help in cases where there is an ambiguity between parsing as roman numerals or alphanumeric (e.g. 'C').",
    ),
    "volumes": (
        "field (integer)",
        "The total number of volumes of a multi-volume work. Depending on the entry type, this field refers to title or maintitle. It is expected to be an integer, not necessarily in arabic numerals since biber will automatically convert from roman numerals or arabic letter to integers internally for sorting purposes. See the noroman option which can be used to suppress roman numeral parsing. This can help in cases where there is an ambiguity between parsing as roman numerals or alphanumeric (e.g. 'C').",
    ),
    "year": (
        "field (literal)",
        "The year of publication. This field is a literal field only when given explicitly in the data (for plain BibTeX compatibility for example). It is however better to use the date field as this is compatible with plain years too and supports many more features.",
    ),
}


# ENTRYS #

## Regular Types ##


### ARTICLE ###

OPTIONAL_FIELDS_ARTICLE = {
    "translator": GENERIC_FIELDS_DESCRIPTION["translator"][1],
    "annotator": GENERIC_FIELDS_DESCRIPTION["annotator"][1],
    "commentator": GENERIC_FIELDS_DESCRIPTION["commentator"][1],
    "subtitle": GENERIC_FIELDS_DESCRIPTION["subtitle"][1],
    "titleaddon": GENERIC_FIELDS_DESCRIPTION["titleaddon"][1],
    "editor": GENERIC_FIELDS_DESCRIPTION["editor"][1],
    "editora": GENERIC_FIELDS_DESCRIPTION["editora"][1],
    "editorb": GENERIC_FIELDS_DESCRIPTION["editorb"][1],
    "editorc": GENERIC_FIELDS_DESCRIPTION["editorc"][1],
    "journalsubtitle": GENERIC_FIELDS_DESCRIPTION["journalsubtitle"][1],
    "journaltitleaddon": GENERIC_FIELDS_DESCRIPTION["journaltitleaddon"][1],
    "issuetitle": GENERIC_FIELDS_DESCRIPTION["issuetitle"][1],
    "issuesubtitle": GENERIC_FIELDS_DESCRIPTION["issuesubtitle"][1],
    "issuetitleaddon": GENERIC_FIELDS_DESCRIPTION["issuetitleaddon"][1],
    "language": GENERIC_FIELDS_DESCRIPTION["language"][1],
    "origlanguage": GENERIC_FIELDS_DESCRIPTION["origlanguage"][1],
    "series": GENERIC_FIELDS_DESCRIPTION["series"][1],
    "volume": GENERIC_FIELDS_DESCRIPTION["volume"][1],
    "number": GENERIC_FIELDS_DESCRIPTION["number"][1],
    "eid": GENERIC_FIELDS_DESCRIPTION["eid"][1],
    "issue": GENERIC_FIELDS_DESCRIPTION["issue"][1],
    "month": GENERIC_FIELDS_DESCRIPTION["month"][1],
    "pages": GENERIC_FIELDS_DESCRIPTION["pages"][1],
    "version": GENERIC_FIELDS_DESCRIPTION["version"][1],
    "note": GENERIC_FIELDS_DESCRIPTION["note"][1],
    "issn": GENERIC_FIELDS_DESCRIPTION["issn"][1],
    "addendum": GENERIC_FIELDS_DESCRIPTION["addendum"][1],
    "pubstate": GENERIC_FIELDS_DESCRIPTION["pubstate"][1],
    "doi": GENERIC_FIELDS_DESCRIPTION["doi"][1],
    "eprint": GENERIC_FIELDS_DESCRIPTION["eprint"][1],
    "eprintclass": GENERIC_FIELDS_DESCRIPTION["eprintclass"][1],
    "eprinttype": GENERIC_FIELDS_DESCRIPTION["eprinttype"][1],
    "url": GENERIC_FIELDS_DESCRIPTION["url"][1],
    "urldate": GENERIC_FIELDS_DESCRIPTION["urldate"][1],
}


@docstring_parameter(
    year=YEAR["type"],
    year_description=YEAR["description"],
    date=DATE["type"],
    date_description=DATE["description"],
    citekey=CITEKEY["type"],
    citekey_description=CITEKEY["description"],
    export=EXPORT["type"],
    export_description=EXPORT["description"],
    optionals=OPTIONALS["type"],
    optionals_description=OPTIONALS["description"],
    citation=CITATION["type"],
    citation_description=CITATION["description"],
    bib=BIB["type"],
    bib_description=BIB["description"],
)
def make_article(
    author,
    title,
    journaltitle,
    citekey,
    year=None,
    date=None,
    export=True,
    **optionals,
):
    """This function generates a `.bib` file for an `@article` entry.

    Parameters
    ----------
    author : str
        The person or persons who wrote the article. The authors' names must be separated by `" and "`;
    title : str
        The name of the article;
    journaltitle : str
        The name of a journal, a newspaper, or some other periodical.
    {year}
        {year_description}
    {date}
        {date_description}
    {citekey}
        {citekey_description}
    {export}
        {export_description}
    {optionals}
        {optionals_description}


    Returns
    -------
    {citation}
        {citation_description}
    {bib}
        {bib_description}


    Notes
    -----
    A list of all optional fields, as well as their description, can be obtained using:

    >>> from normtest import bibmaker
    >>> for key, value in bibmaker.OPTIONAL_FIELDS_ARTICLE.items():
    >>>     print(key, ": ", value)


    """

    if year is None and date is None:
        try:
            raise ValueError("FieldNotFoundError")
        except ValueError:
            print("Parameters `year` and `date` cannot be `None` at the same time.\n")
            raise

    field_template = "  {field_tag}{spaces} = {{{tag_value}}},\n"

    fields = {
        "author": author,
        "title": title,
        "journaltitle": journaltitle,
        "year": year,
        "date": date,
    }
    # getting all fields types
    optional_fields = dict.fromkeys(OPTIONAL_FIELDS_ARTICLE.keys())
    optional_fields.update(optionals)
    fields.update(optional_fields)

    filtered = {k: v for k, v in fields.items() if v is not None}
    fields.clear()
    fields.update(filtered)

    # building the citation
    # first line:
    citation = ["@article{{{citekey},\n".format(citekey=citekey)]

    # ading fields
    for key, value in fields.items():
        spaces = " " * empty_spaces(fields.keys(), key)
        citation.append(
            field_template.format(field_tag=key, spaces=spaces, tag_value=value)
        )
    citation[-1] = citation[-1][:-2] + citation[-1][-1:]

    citation.append("}")

    if export:
        with open(f"{citekey}.bib", "w") as my_bib:
            for i in range(len(citation)):
                my_bib.write(f"{citation[i]}")

    return """""".join(citation)


### BOOK ###

OPTIONAL_FIELDS_BOOK = {
    "editor": GENERIC_FIELDS_DESCRIPTION["editor"][1],
    "editora": GENERIC_FIELDS_DESCRIPTION["editora"][1],
    "editorb": GENERIC_FIELDS_DESCRIPTION["editorb"][1],
    "editorc": GENERIC_FIELDS_DESCRIPTION["editorc"][1],
    "translator": GENERIC_FIELDS_DESCRIPTION["translator"][1],
    "annotator": GENERIC_FIELDS_DESCRIPTION["annotator"][1],
    "commentator": GENERIC_FIELDS_DESCRIPTION["commentator"][1],
    "introduction": GENERIC_FIELDS_DESCRIPTION["introduction"][1],
    "foreword": GENERIC_FIELDS_DESCRIPTION["foreword"][1],
    "afterword": GENERIC_FIELDS_DESCRIPTION["afterword"][1],
    "subtitle": GENERIC_FIELDS_DESCRIPTION["subtitle"][1],
    "titleaddon": GENERIC_FIELDS_DESCRIPTION["titleaddon"][1],
    "maintitle": GENERIC_FIELDS_DESCRIPTION["maintitle"][1],
    "mainsubtitle": GENERIC_FIELDS_DESCRIPTION["mainsubtitle"][1],
    "maintitleaddon": GENERIC_FIELDS_DESCRIPTION["maintitleaddon"][1],
    "language": GENERIC_FIELDS_DESCRIPTION["language"][1],
    "origlanguage": GENERIC_FIELDS_DESCRIPTION["origlanguage"][1],
    "volume": GENERIC_FIELDS_DESCRIPTION["volume"][1],
    "part": GENERIC_FIELDS_DESCRIPTION["part"][1],
    "edition": GENERIC_FIELDS_DESCRIPTION["edition"][1],
    "volumes": GENERIC_FIELDS_DESCRIPTION["volumes"][1],
    "series": GENERIC_FIELDS_DESCRIPTION["series"][1],
    "number": GENERIC_FIELDS_DESCRIPTION["number"][1],
    "note": GENERIC_FIELDS_DESCRIPTION["note"][1],
    "publisher": GENERIC_FIELDS_DESCRIPTION["publisher"][1],
    "location": GENERIC_FIELDS_DESCRIPTION["location"][1],
    "isbn": GENERIC_FIELDS_DESCRIPTION["isbn"][1],
    "eid": GENERIC_FIELDS_DESCRIPTION["eid"][1],
    "chapter": GENERIC_FIELDS_DESCRIPTION["chapter"][1],
    "pages": GENERIC_FIELDS_DESCRIPTION["pages"][1],
    "pagetotal": GENERIC_FIELDS_DESCRIPTION["pagetotal"][1],
    "addendum": GENERIC_FIELDS_DESCRIPTION["addendum"][1],
    "pubstate": GENERIC_FIELDS_DESCRIPTION["pubstate"][1],
    "doi": GENERIC_FIELDS_DESCRIPTION["doi"][1],
    "eprint": GENERIC_FIELDS_DESCRIPTION["eprint"][1],
    "eprintclass": GENERIC_FIELDS_DESCRIPTION["eprintclass"][1],
    "eprinttype": GENERIC_FIELDS_DESCRIPTION["eprinttype"][1],
    "url": GENERIC_FIELDS_DESCRIPTION["url"][1],
    "urldate": GENERIC_FIELDS_DESCRIPTION["urldate"][1],
}


@docstring_parameter(
    year=YEAR["type"],
    year_description=YEAR["description"],
    date=DATE["type"],
    date_description=DATE["description"],
    citekey=CITEKEY["type"],
    citekey_description=CITEKEY["description"],
    export=EXPORT["type"],
    export_description=EXPORT["description"],
    optionals=OPTIONALS["type"],
    optionals_description=OPTIONALS["description"],
    citation=CITATION["type"],
    citation_description=CITATION["description"],
    bib=BIB["type"],
    bib_description=BIB["description"],
)
def make_book(
    author,
    title,
    citekey,
    year=None,
    date=None,
    export=True,
    **optionals,
):
    """This function generates a `.bib` file for an `@book` entry.

    Parameters
    ----------
    author : str
        The person or persons who wrote the book. The authors' names must be separated by `" and "`;
    title : str
        The name of the book;
    {year}
        {year_description}
    {date}
        {date_description}
    {citekey}
        {citekey_description}
    {export}
        {export_description}
    {optionals}
        {optionals_description}


    Returns
    -------
    {citation}
        {citation_description}
    {bib}
        {bib_description}


    Notes
    -----
    A list of all optional fields, as well as their description, can be obtained using:

    >>> from normtest import bibmaker
    >>> for key, value in bibmaker.OPTIONAL_FIELDS_BOOK.items():
    >>>     print(key, ": ", value)

    Examples
    --------



    """

    if year is None and date is None:
        try:
            raise ValueError("FieldNotFoundError")
        except ValueError:
            print("Parameters `year` and `date` cannot be `None` at the same time.\n")
            raise

    field_template = "  {field_tag}{spaces} = {{{tag_value}}},\n"

    fields = {
        "author": author,
        "title": title,
        "year": year,
        "date": date,
    }
    # getting all fields types
    optional_fields = dict.fromkeys(OPTIONAL_FIELDS_BOOK.keys())
    optional_fields.update(optionals)
    fields.update(optional_fields)

    filtered = {k: v for k, v in fields.items() if v is not None}
    fields.clear()
    fields.update(filtered)

    # building the citation
    # first line:
    citation = ["@book{{{citekey},\n".format(citekey=citekey)]

    # ading fields
    for key, value in fields.items():
        spaces = " " * empty_spaces(fields.keys(), key)
        citation.append(
            field_template.format(field_tag=key, spaces=spaces, tag_value=value)
        )
    citation[-1] = citation[-1][:-2] + citation[-1][-1:]

    citation.append("}")

    if export:
        with open(f"{citekey}.bib", "w") as my_bib:
            for i in range(len(citation)):
                my_bib.write(f"{citation[i]}")

    return """""".join(citation)


### TECHREPORT ###

OPTIONAL_FIELDS_TECHREPORT = {
    "type": GENERIC_FIELDS_DESCRIPTION["type"][1],
    "subtitle": GENERIC_FIELDS_DESCRIPTION["subtitle"][1],
    "titleaddon": GENERIC_FIELDS_DESCRIPTION["titleaddon"][1],
    "language": GENERIC_FIELDS_DESCRIPTION["language"][1],
    "number": GENERIC_FIELDS_DESCRIPTION["number"][1],
    "version": GENERIC_FIELDS_DESCRIPTION["version"][1],
    "note": GENERIC_FIELDS_DESCRIPTION["note"][1],
    "location": GENERIC_FIELDS_DESCRIPTION["location"][1],
    "month": GENERIC_FIELDS_DESCRIPTION["month"][1],
    "isrn": GENERIC_FIELDS_DESCRIPTION["isrn"][1],
    "eid": GENERIC_FIELDS_DESCRIPTION["eid"][1],
    "chapter": GENERIC_FIELDS_DESCRIPTION["chapter"][1],
    "pages": GENERIC_FIELDS_DESCRIPTION["pages"][1],
    "pagetotal": GENERIC_FIELDS_DESCRIPTION["pagetotal"][1],
    "addendum": GENERIC_FIELDS_DESCRIPTION["addendum"][1],
    "pubstate": GENERIC_FIELDS_DESCRIPTION["pubstate"][1],
    "doi": GENERIC_FIELDS_DESCRIPTION["doi"][1],
    "eprint": GENERIC_FIELDS_DESCRIPTION["eprint"][1],
    "eprintclass": GENERIC_FIELDS_DESCRIPTION["eprintclass"][1],
    "eprinttype": GENERIC_FIELDS_DESCRIPTION["eprinttype"][1],
    "url": GENERIC_FIELDS_DESCRIPTION["url"][1],
    "urldate": GENERIC_FIELDS_DESCRIPTION["urldate"][1],
}


@docstring_parameter(
    year=YEAR["type"],
    year_description=YEAR["description"],
    date=DATE["type"],
    date_description=DATE["description"],
    citekey=CITEKEY["type"],
    citekey_description=CITEKEY["description"],
    export=EXPORT["type"],
    export_description=EXPORT["description"],
    optionals=OPTIONALS["type"],
    optionals_description=OPTIONALS["description"],
    citation=CITATION["type"],
    citation_description=CITATION["description"],
    bib=BIB["type"],
    bib_description=BIB["description"],
)
def make_techreport(
    author,
    title,
    institution,
    citekey,
    year=None,
    date=None,
    export=True,
    **optionals,
):
    """This function generates a `.bib` file for an `@techreport` entry.

    Parameters
    ----------
    author : str
        The person or persons who wrote the techreport. The authors' names must be separated by `" and "`;
    title : str
        The name of the techreport;
    institution : str
        The name of a university or some other institution, depending on the entry type. Traditional BibTeX uses the field name school for theses, which is supported as analias.
    {year}
        {year_description}
    {date}
        {date_description}
    {citekey}
        {citekey_description}
    {export}
        {export_description}
    {optionals}
        {optionals_description}


    Returns
    -------
    {citation}
        {citation_description}
    {bib}
        {bib_description}


    Notes
    -----
    A list of all optional fields, as well as their description, can be obtained using:

    >>> from normtest import bibmaker
    >>> for key, value in bibmaker.OPTIONAL_FIELDS_TECHREPORT.items():
    >>>     print(key, ": ", value)



    """

    if year is None and date is None:
        try:
            raise ValueError("FieldNotFoundError")
        except ValueError:
            print("Parameters `year` and `date` cannot be `None` at the same time.\n")
            raise

    field_template = "  {field_tag}{spaces} = {{{tag_value}}},\n"

    fields = {
        "author": author,
        "title": title,
        "institution": institution,
        "year": year,
        "date": date,
    }
    # getting all fields types
    optional_fields = dict.fromkeys(OPTIONAL_FIELDS_TECHREPORT.keys())
    optional_fields.update(optionals)
    fields.update(optional_fields)

    filtered = {k: v for k, v in fields.items() if v is not None}
    fields.clear()
    fields.update(filtered)

    # building the citation
    # first line:
    citation = ["@techreport{{{citekey},\n".format(citekey=citekey)]

    # ading fields
    for key, value in fields.items():
        spaces = " " * empty_spaces(fields.keys(), key)
        citation.append(
            field_template.format(field_tag=key, spaces=spaces, tag_value=value)
        )
    citation[-1] = citation[-1][:-2] + citation[-1][-1:]

    citation.append("}")

    if export:
        with open(f"{citekey}.bib", "w") as my_bib:
            for i in range(len(citation)):
                my_bib.write(f"{citation[i]}")

    return """""".join(citation)


### MVBOOK ###

OPTIONAL_FIELDS_MVBOOK = {
    "editor": GENERIC_FIELDS_DESCRIPTION["editor"][1],
    "editora": GENERIC_FIELDS_DESCRIPTION["editora"][1],
    "editorb": GENERIC_FIELDS_DESCRIPTION["editorb"][1],
    "editorc": GENERIC_FIELDS_DESCRIPTION["editorc"][1],
    "translator": GENERIC_FIELDS_DESCRIPTION["translator"][1],
    "annotator": GENERIC_FIELDS_DESCRIPTION["annotator"][1],
    "commentator": GENERIC_FIELDS_DESCRIPTION["commentator"][1],
    "introduction": GENERIC_FIELDS_DESCRIPTION["introduction"][1],
    "foreword": GENERIC_FIELDS_DESCRIPTION["foreword"][1],
    "afterword": GENERIC_FIELDS_DESCRIPTION["afterword"][1],
    "subtitle": GENERIC_FIELDS_DESCRIPTION["subtitle"][1],
    "titleaddon": GENERIC_FIELDS_DESCRIPTION["titleaddon"][1],
    "language": GENERIC_FIELDS_DESCRIPTION["language"][1],
    "origlanguage": GENERIC_FIELDS_DESCRIPTION["origlanguage"][1],
    "edition": GENERIC_FIELDS_DESCRIPTION["edition"][1],
    "volumes": GENERIC_FIELDS_DESCRIPTION["volumes"][1],
    "series": GENERIC_FIELDS_DESCRIPTION["series"][1],
    "number": GENERIC_FIELDS_DESCRIPTION["number"][1],
    "note": GENERIC_FIELDS_DESCRIPTION["note"][1],
    "publisher": GENERIC_FIELDS_DESCRIPTION["publisher"][1],
    "location": GENERIC_FIELDS_DESCRIPTION["location"][1],
    "isbn": GENERIC_FIELDS_DESCRIPTION["isbn"][1],
    "pagetotal": GENERIC_FIELDS_DESCRIPTION["pagetotal"][1],
    "addendum": GENERIC_FIELDS_DESCRIPTION["addendum"][1],
    "pubstate": GENERIC_FIELDS_DESCRIPTION["pubstate"][1],
    "doi": GENERIC_FIELDS_DESCRIPTION["doi"][1],
    "eprint": GENERIC_FIELDS_DESCRIPTION["eprint"][1],
    "eprintclass": GENERIC_FIELDS_DESCRIPTION["eprintclass"][1],
    "eprinttype": GENERIC_FIELDS_DESCRIPTION["eprinttype"][1],
    "url": GENERIC_FIELDS_DESCRIPTION["url"][1],
    "urldate": GENERIC_FIELDS_DESCRIPTION["urldate"][1],
}


def make_mvbook(
    author,
    title,
    citekey,
    year=None,
    date=None,
    export=True,
    **optionals,
):
    """This function generates a `.bib` file for an `@mvbook` entry.

    Parameters
    ----------
    author : str
        The person or persons who wrote the  multi-volume book. The authors' names must be separated by `" and "`;
    title : str
        The name of the multi-volume book;
    year : int, optional
        The year of publication; If `year=None`, the `date` parameter must not be `None`;
    date : str, optional
        The publication date. If `date=None`, the `year` parameter must not be `None`;
    citekey : str
        The name that is used to uniquely identify the entry. If None, the algorithm will generate an automatic `citekey` based on the name of the authors and the year. See Notes for details;
    export : bool, optional
        Whether to export the `citekey.bib` file (`True`, default) or not (`False`);
    **optionals : str
        Optional fields for an article entry (`volume`, `number`, `pages`, etc).


    Returns
    -------
    citation : str
        The citation generated
    bib : file
        The `citekey.bib` file (only if `export=True`)


    Notes
    -----
    A list of all optional fields, as well as their description, can be obtained using:

    >>> from normtest import bibmaker
    >>> for key, value in bibmaker.OPTIONAL_FIELDS_MVBOOK.items():
    >>>     print(key, ": ", value)


    """

    if year is None and date is None:
        try:
            raise ValueError("FieldNotFoundError")
        except ValueError:
            print("Parameters `year` and `date` cannot be `None` at the same time.\n")
            raise

    field_template = "  {field_tag}{spaces} = {{{tag_value}}},\n"

    fields = {
        "author": author,
        "title": title,
        "year": year,
        "date": date,
    }
    # getting all fields types
    optional_fields = dict.fromkeys(OPTIONAL_FIELDS_MVBOOK.keys())
    optional_fields.update(optionals)
    fields.update(optional_fields)

    filtered = {k: v for k, v in fields.items() if v is not None}
    fields.clear()
    fields.update(filtered)

    # building the citation
    # first line:
    citation = ["@mvbook{{{citekey},\n".format(citekey=citekey)]

    # ading fields
    for key, value in fields.items():
        spaces = " " * empty_spaces(fields.keys(), key)
        citation.append(
            field_template.format(field_tag=key, spaces=spaces, tag_value=value)
        )
    citation[-1] = citation[-1][:-2] + citation[-1][-1:]

    citation.append("}")

    if export:
        with open(f"{citekey}.bib", "w") as my_bib:
            for i in range(len(citation)):
                my_bib.write(f"{citation[i]}")

    return """""".join(citation)
