//////////////////////////////////////////////////////////////////////////
//
//  Copyright (c) 2017, Image Engine Design Inc. All rights reserved.
//
//  Redistribution and use in source and binary forms, with or without
//  modification, are permitted provided that the following conditions are
//  met:
//
//      * Redistributions of source code must retain the above
//        copyright notice, this list of conditions and the following
//        disclaimer.
//
//      * Redistributions in binary form must reproduce the above
//        copyright notice, this list of conditions and the following
//        disclaimer in the documentation and/or other materials provided with
//        the distribution.
//
//      * Neither the name of John Haddon nor the names of
//        any other contributors to this software may be used to endorse or
//        promote products derived from this software without specific prior
//        written permission.
//
//  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS
//  IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO,
//  THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
//  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR
//  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL,
//  EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
//  PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR
//  PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF
//  LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
//  NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
//  SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
//////////////////////////////////////////////////////////////////////////

#include "boost/python.hpp"

#include "FilterBinding.h"

#include "GafferScene/Filter.h"
#include "GafferScene/FilterPlug.h"
#include "GafferScene/FilterProcessor.h"
#include "GafferScene/FilterResults.h"
#include "GafferScene/PathFilter.h"
#include "GafferScene/ScenePlug.h"
#include "GafferScene/SetFilter.h"
#include "GafferScene/UnionFilter.h"

#include "GafferBindings/DependencyNodeBinding.h"
#include "GafferBindings/PlugBinding.h"

using namespace boost::python;
using namespace Gaffer;
using namespace GafferBindings;
using namespace GafferScene;

namespace
{

ScenePlugPtr getInputScene( const Gaffer::Context *context )
{
	return const_cast<ScenePlug *>( Filter::getInputScene( context ) );
}

int match( const FilterPlug &plug, const ScenePlug &scene )
{
	IECorePython::ScopedGILRelease r;
	return plug.match( &scene );
}


} // namespace

void GafferSceneModule::bindFilter()
{

	GafferBindings::DependencyNodeClass<Filter>()
		.def( "setInputScene", &Filter::setInputScene )
		.staticmethod( "setInputScene" )
		.def( "getInputScene", &getInputScene )
		.staticmethod( "getInputScene" )
	;

	PlugClass<FilterPlug>()
		.def( init<const std::string &, Plug::Direction, unsigned>(
				(
					arg( "name" ) = Gaffer::GraphComponent::defaultName<FilterPlug>(),
					arg( "direction" ) = Gaffer::Plug::In,
					arg( "flags" ) = Gaffer::Plug::Default
				)
			)
		)
		.def( init<const std::string &, Plug::Direction, int, int, int, unsigned>(
				(
					arg( "name" ) = Gaffer::GraphComponent::defaultName<FilterPlug>(),
					arg( "direction" ) = Gaffer::Plug::In,
					arg( "defaultValue" ) = IECore::PathMatcher::NoMatch,
					arg( "minValue" ) = IECore::PathMatcher::NoMatch,
					arg( "maxValue" ) = IECore::PathMatcher::EveryMatch,
					arg( "flags" ) = Gaffer::Plug::Default
				)
			)
		)
		.def( "match", &match )
	;

	GafferBindings::DependencyNodeClass<PathFilter>();
	GafferBindings::DependencyNodeClass<FilterProcessor>();
	GafferBindings::DependencyNodeClass<UnionFilter>();
	GafferBindings::DependencyNodeClass<SetFilter>();
	GafferBindings::DependencyNodeClass<FilterResults>();
}
