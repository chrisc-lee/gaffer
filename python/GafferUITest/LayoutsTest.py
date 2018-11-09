##########################################################################
#
#  Copyright (c) 2018, Image Engine Design Inc. All rights reserved.
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
#
#      * Redistributions of source code must retain the above
#        copyright notice, this list of conditions and the following
#        disclaimer.
#
#      * Redistributions in binary form must reproduce the above
#        copyright notice, this list of conditions and the following
#        disclaimer in the documentation and/or other materials provided with
#        the distribution.
#
#      * Neither the name of John Haddon nor the names of
#        any other contributors to this software may be used to endorse or
#        promote products derived from this software without specific prior
#        written permission.
#
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
#  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
#  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
#  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
#  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
#  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
#  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
#  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
#  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
#  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
#  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
##########################################################################

import os

import Gaffer
import GafferUI
import GafferUITest

class LayoutsTest( GafferUITest.TestCase ) :

	def testAcquire( self ) :

		a = Gaffer.ApplicationRoot( "testApp" )
		self.assertIsInstance( GafferUI.Layouts.acquire( a ), GafferUI.Layouts )
		self.assertIs( GafferUI.Layouts.acquire( a ), GafferUI.Layouts.acquire( a ) )

	def testAddAndRemove( self ) :

		a = Gaffer.ApplicationRoot( "testApp" )
		l = GafferUI.Layouts.acquire( a )
		self.assertEqual( l.names(), [] )

		l.add( "JustTheGraphEditor", "GafferUI.GraphEditor( script )" )
		self.assertEqual( l.names(), [ "JustTheGraphEditor" ] )

		l.add( "JustTheNodeEditor", "GafferUI.NodeEditor( script )" )
		self.assertEqual( l.names(), [ "JustTheGraphEditor", "JustTheNodeEditor" ] )

		l.remove( "JustTheGraphEditor" )
		self.assertEqual( l.names(), [ "JustTheNodeEditor" ] )

		l.remove( "JustTheNodeEditor" )
		self.assertEqual( l.names(), [] )

	def testPersistence( self ) :

		a = Gaffer.ApplicationRoot( "testApp" )
		l = GafferUI.Layouts.acquire( a )
		self.assertEqual( l.names(), [] )

		l.add( "JustTheGraphEditor", "GafferUI.GraphEditor( script )" )
		self.assertEqual( l.names(), [ "JustTheGraphEditor" ] )
		self.assertEqual( l.names( persistent = False ), [ "JustTheGraphEditor" ] )
		self.assertEqual( l.names( persistent = True ), [] )

		l.add( "JustTheNodeEditor", "GafferUI.NodeEditor( script )", persistent = True )
		self.assertEqual( l.names(), [ "JustTheGraphEditor", "JustTheNodeEditor" ] )
		self.assertEqual( l.names( persistent = False ), [ "JustTheGraphEditor" ] )
		self.assertEqual( l.names( persistent = True ), [ "JustTheNodeEditor" ] )

	def testNoPersistentLayoutsInDefaultConfigs( self ) :

		class TestApp( Gaffer.Application ) :

			def __init__( self ) :

				Gaffer.Application.__init__( self, "Test" )

			def _run( self, args ) :

				# Load the standard gui config files
				self._executeStartupFiles( "gui" )

				return 0

		app = TestApp()

		# Load the GUI config, making sure we only use the standard
		# startup files, and not any others from the current environment
		# (the user running these tests may have their own personal configs).
		startupPaths = os.environ["GAFFER_STARTUP_PATHS"]
		try :
			os.environ["GAFFER_STARTUP_PATHS"] = os.path.expandvars( "$GAFFER_ROOT/startup" )
			app.run()
		finally :
			os.environ["GAFFER_STARTUP_PATHS"] = startupPaths

		self.assertEqual( os.environ["GAFFER_STARTUP_PATHS"], startupPaths )

		layouts = GafferUI.Layouts.acquire( app )
		self.assertEqual( layouts.names( persistent = True ), [] )
		self.assertGreater( len( layouts.names() ), 0 )

if __name__ == "__main__":
	unittest.main()
