<?xml version="1.0" encoding="utf-8"?>
<!--http://www.jenitennison.com/xslt/grouping/muenchian.html -->
<xsl:stylesheet version="1.0"
  xmlns:atom="http://www.w3.org/2005/Atom"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:dc="http://purl.org/dc/elements/1.1/">
  <xsl:output method="xml"/>
  <xsl:template match="/">
    <xsl:apply-templates select="/atom:feed"/>
  </xsl:template>
  <xsl:key name="year" match="atom:entry" use="substring(atom:published, 0, 5)" />
  <xsl:key name="month" match="atom:entry" use="substring(atom:published, 0, 8)" />
  <xsl:key name="day" match="atom:entry" use="substring(atom:published, 0, 11)" />
  <xsl:template match="/atom:feed">
    <ul>
      <xsl:for-each select="atom:entry[count(. | key('year', substring(atom:published, 0, 5))[1]) = 1]">
        <xsl:sort select="substring(atom:published, 0, 5)" order="descending"/>
            <li class="Treeview-Root">
                <span class="TreeView-Expand" onclick="ExpandCollapse_TreeView(this)">&#160;</span>
                <xsl:value-of select="substring(atom:published, 0, 5)" /> (<xsl:value-of select="count(key('year', substring(atom:published, 0, 5)))"/>)
                <ul class="TreeView-Hide">
                    <xsl:for-each select="key('year', substring(atom:published, 0, 5))[count(. | key('month', substring(atom:published, 0, 8))[1]) = 1]">
                    <xsl:sort select="substring(atom:published, 6, 2)" order="descending"/>
                        <li class="Treeview-Root">
                            <span class="TreeView-Collapse" onclick="ExpandCollapse_TreeView(this)">&#160;</span>            
                            <xsl:call-template name="decode">
                                <xsl:with-param name="id">
                                <xsl:value-of select="substring(atom:published, 6, 2)" />
                            </xsl:with-param>
                            <xsl:with-param name="locale">it</xsl:with-param>
                            </xsl:call-template> (<xsl:value-of select="count(key('month', substring(atom:published, 0, 8)))"/>)
                            <ul>
                                <xsl:for-each select="key('month', substring(atom:published, 0, 8))[count(. | key('day', substring(atom:published, 0, 11))[1]) = 1]">
                                <xsl:sort select="substring(atom:published, 0, 11)" order="descending"/>
                                    <li class="Treeview-Root">
                                        <span class="TreeView-Collapse" onclick="ExpandCollapse_TreeView(this)">&#160;</span>            
                                        <xsl:value-of select="substring(atom:published, 9, 2)" /> (<xsl:value-of select="count(key('day', substring(atom:published, 0, 11)))"/>)
                                        <ul>
                                            <xsl:for-each select="key('day', substring(atom:published, 0, 11))">
                                            <xsl:sort select="substring(atom:published, 9, 2)" />
                                                <li class="Treeview-Root">
                                                    <a>
                                                        <xsl:attribute name="href">?post_id=<xsl:value-of select="atom:id" /></xsl:attribute>
                                                        <xsl:value-of select="atom:title" />
                                                    </a>
                                                </li>
                                        </xsl:for-each>
                                        </ul>
                                    </li>
                                </xsl:for-each>
                            </ul>
                        </li>
                    </xsl:for-each>
                </ul>
            </li>    
        </xsl:for-each>
    </ul>
  </xsl:template>
  <xsl:template name="decode">
    <xsl:param name="id"/>
    <xsl:param name="locale"/>
	  <xsl:choose>
		  <xsl:when test="$locale = 'us'">
			  <xsl:choose>
				  <xsl:when test="$id = 01">
					  january
				  </xsl:when>
				  <xsl:when test="$id = 02">
					  february
				  </xsl:when>
				  <xsl:when test="$id = 03">
					  march
				  </xsl:when>
				  <xsl:when test="$id = 04">
					  april
				  </xsl:when>
				  <xsl:when test="$id = 05">
					  may
				  </xsl:when>
				  <xsl:when test="$id = 06">
					  june
				  </xsl:when>
				  <xsl:when test="$id = 07">
					  july
				  </xsl:when>
				  <xsl:when test="$id = 08">
					  august
				  </xsl:when>
				  <xsl:when test="$id = 09">
					  september
				  </xsl:when>
				  <xsl:when test="$id = 10">
					  october
				  </xsl:when>
				  <xsl:when test="$id = 11">
					  november
				  </xsl:when>
				  <xsl:when test="$id = 12">
					  december
				  </xsl:when>
				  <xsl:otherwise>
					  wrong month id
				  </xsl:otherwise>
			  </xsl:choose>

		  </xsl:when>
		  <xsl:when test="$locale = 'it'">
			  <xsl:choose>
				  <xsl:when test="$id = 01">gennaio</xsl:when>
				  <xsl:when test="$id = 02">febbraio</xsl:when>
				  <xsl:when test="$id = 03">marzo</xsl:when>
				  <xsl:when test="$id = 04">aprile</xsl:when>
				  <xsl:when test="$id = 05">maggio</xsl:when>
				  <xsl:when test="$id = 06">giugno</xsl:when>
				  <xsl:when test="$id = 07">luglio</xsl:when>
				  <xsl:when test="$id = 08">agosto</xsl:when>
				  <xsl:when test="$id = 09">settembre</xsl:when>
				  <xsl:when test="$id = 10">ottobre</xsl:when>
				  <xsl:when test="$id = 11">novembre</xsl:when>
				  <xsl:when test="$id = 12">dicembre</xsl:when>
				  <xsl:otherwise>id del mese errato</xsl:otherwise>
			  </xsl:choose>

		  </xsl:when>
	  </xsl:choose>

  </xsl:template>
</xsl:stylesheet>
