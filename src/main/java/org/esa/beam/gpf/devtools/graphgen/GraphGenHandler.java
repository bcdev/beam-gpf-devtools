/*
 * Copyright (C) 2011 Brockmann Consult GmbH (info@brockmann-consult.de)
 *
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 3 of the License, or (at your option)
 * any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 *
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, see http://www.gnu.org/licenses/
 */
package org.esa.beam.gpf.devtools.graphgen;

import org.esa.beam.framework.datamodel.Band;
import org.esa.beam.framework.datamodel.Product;

/**
 * Handles various events fired by the {@link GraphGen} class.
 *
 * @author Thomas Storm
 * @author Norman Fomferra
 */
public interface GraphGenHandler {

    void handleBeginGraph();

    void handleEndGraph();

    void generateOpNode(Op operator);

    void generateProductNode(Product product);

    void generateOp2BandEdge(Op operator, Band band);

    void generateOp2ProductEdge(Op operator, Product product);

    void generateProduct2OpEdge(Product sourceProduct, Op operator);

    void generateOp2OpEdge(Op source, Op target);
}
